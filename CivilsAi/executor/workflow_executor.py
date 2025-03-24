import grpc
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from cache.workflow_cached_data import CACHE_EXPIRATION
from utils.postgress_conn import db_instance, redis_client
from models.sql_models import Workflow, Task, WorkflowStatus, ExecutionType
import workflow_pb2, workflow_pb2_grpc


class WorkflowExecutorServicer(workflow_pb2_grpc.WorkflowExecutorServicer):
    def ExecuteWorkflow(self, request, context):
        workflow_name = request.workflow_name
        db = next(db_instance.get_db())

        # Check cache first
        cached_status = redis_client.get(f"workflow_status:{workflow_name}")
        if cached_status and cached_status == "COMPLETED":
            return workflow_pb2.ExecuteResponse(
                message="Workflow already completed", status="COMPLETED"
            )

        workflow = db.query(Workflow).filter(Workflow.name == workflow_name).first()
        if not workflow:
            return workflow_pb2.ExecuteResponse(
                message="Workflow not found", status="FAILED"
            )

        workflow.status = WorkflowStatus.IN_PROGRESS
        db.commit()
        redis_client.setex(f"workflow_status:{workflow_name}", CACHE_EXPIRATION, "IN_PROGRESS")

        tasks = db.query(Task).filter(Task.workflow_name == workflow_name).order_by(Task.order).all()

        # Track async tasks separately
        async_tasks = []
        
        for task in tasks:
            if task.execution_type == ExecutionType.SYNC:
                self._execute_task(task)
            else:
                async_task = threading.Thread(target=self._execute_task, args=(task,))
                async_task.start()
                async_tasks.append(async_task)

        # Wait for all async tasks to complete
        for task in async_tasks:
            task.join()

        workflow.status = WorkflowStatus.COMPLETED
        db.commit()
        redis_client.setex(f"workflow_status:{workflow_name}", CACHE_EXPIRATION, "COMPLETED")

        return workflow_pb2.ExecuteResponse(
            message="Workflow executed successfully", status="COMPLETED"
        )

    def _execute_task(self, task):
        print(f"Executing Task: {task.name}")
        time.sleep(2)  # Simulating execution time
        print(f"Completed Task: {task.name}")

    def GetWorkflowStatus(self, request, context):
        workflow_name = request.workflow_name
        cached_status = redis_client.get(f"workflow_status:{workflow_name}")
        if cached_status:
            return workflow_pb2.StatusResponse(status=cached_status)

        db = next(db_instance.get_db())

        workflow = db.query(Workflow).filter(Workflow.name == workflow_name).first()
        if not workflow:
            return workflow_pb2.StatusResponse(status="NOT_FOUND")

        redis_client.setex(f"workflow_status:{workflow_name}", CACHE_EXPIRATION, workflow.status.value)
        return workflow_pb2.StatusResponse(status=workflow.status.value)
