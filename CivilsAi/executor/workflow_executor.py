import grpc
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.orm import Session
from database import db_instance
from model import Workflow, Task, WorkflowStatus, ExecutionType
import workflow_pb2, workflow_pb2_grpc

class WorkflowExecutorServicer(workflow_pb2_grpc.WorkflowExecutorServicer):
    def ExecuteWorkflow(self, request, context):
        workflow_id = request.workflow_id
        db = next(db_instance.get_db())

        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            return workflow_pb2.ExecuteResponse(
                message="Workflow not found", status="FAILED"
            )

        workflow.status = WorkflowStatus.IN_PROGRESS
        db.commit()

        tasks = db.query(Task).filter(Task.workflow_id == workflow_id).order_by(Task.order).all()

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

        return workflow_pb2.ExecuteResponse(
            message="Workflow executed successfully", status="COMPLETED"
        )

    def _execute_task(self, task):
        print(f"Executing Task: {task.name}")
        time.sleep(2)  # Simulating execution time
        print(f"Completed Task: {task.name}")

    def GetWorkflowStatus(self, request, context):
        workflow_id = request.workflow_id
        db = next(db_instance.get_db())

        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            return workflow_pb2.StatusResponse(status="NOT_FOUND")

        return workflow_pb2.StatusResponse(status=workflow.status.value)