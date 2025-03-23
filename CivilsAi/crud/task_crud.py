from sqlalchemy.orm import Session
from cache.workflow_cached_data import invalidate_workflow_cache
from models.sql_models import Task, Workflow
from utils.schemas import TaskCreate, TaskUpdate
import logging
from sqlalchemy.exc import SQLAlchemyError
# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def add_task_to_workflow(db: Session, workflow_name: str, task_data: TaskCreate):
    try:
        workflow = db.query(Workflow).filter(Workflow.name == workflow_name).first()
        if not workflow:
            return None

        task = Task(
            name=task_data.name,
            description=task_data.description,
            order=task_data.order,
            execution_type=task_data.execution_type,
            workflow_name=workflow_name
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        invalidate_workflow_cache(workflow_name)  # Invalidate cache on update
        return task
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error adding task to workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to add task to workflow"}

def update_task(db: Session, workflow_name: str, task_name: str, task_data: TaskUpdate):
    try:
        task = db.query(Task).filter(Task.workflow_name == workflow_name, Task.name == task_name).first()
        if not task:
            return None

        if task_data.name is not None:
            task.name = task_data.name
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.order is not None:
            task.order = task_data.order
        if task_data.execution_type is not None:
            task.execution_type = task_data.execution_type

        db.commit()
        db.refresh(task)

        invalidate_workflow_cache(task.workflow_name)  # Invalidate cache on update
        return {"message": "Task updated successfully", "task": task}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating task {task_name} in workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to update task"}

def delete_task(db: Session, workflow_name: str, task_name: str):
    try:
        task = db.query(Task).filter(Task.workflow_name == workflow_name, Task.name == task_name).first()
        if not task:
            return None

        db.delete(task)
        db.commit()

        invalidate_workflow_cache(workflow_name)  # Invalidate cache on delete
        return {"message": "Task deleted successfully"}

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting task {task_name} from workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to delete task"}