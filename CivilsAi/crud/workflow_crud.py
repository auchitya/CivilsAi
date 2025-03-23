from sqlalchemy.orm import Session
from cache.workflow_cached_data import cache_workflow, get_cached_workflow, invalidate_workflow_cache
from models.sql_models import Workflow
from utils.schemas import WorkflowCreate
from sqlalchemy.orm import joinedload
import logging
from sqlalchemy.exc import SQLAlchemyError


# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def get_workflow(db: Session, workflow_name: str):
    try:
        cached_data = get_cached_workflow(workflow_name)
        if cached_data:
            return cached_data  # Return from cache if available

        workflow = db.query(Workflow).options(joinedload(Workflow.tasks)).filter(Workflow.name == workflow_name).first()
        if workflow:
            cache_workflow(workflow)  # Store in cache
        return workflow
    except SQLAlchemyError as e:
        logger.error(f"Error fetching workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to fetch workflow"}

def create_workflow(db: Session, workflow_data: WorkflowCreate):
    try:
        existing_workflow = db.query(Workflow).filter(Workflow.name == workflow_data.name).first()
        if existing_workflow:
            return {"message": "Workflow already exists"}

        workflow = Workflow(name=workflow_data.name)
        db.add(workflow)
        db.commit()
        db.refresh(workflow)

        cache_workflow(workflow)  # Cache new workflow
        return workflow
    except SQLAlchemyError as e:
        db.rollback()  # Rollback in case of failure
        logger.error(f"Error creating workflow: {str(e)}")
        return {"error": "Failed to create workflow"}

def update_workflow(db: Session, workflow_name: str, name: str):
    try:
        workflow = db.query(Workflow).filter(Workflow.name == workflow_name).first()
        if workflow:
            workflow.name = name
            db.commit()
            db.refresh(workflow)
            invalidate_workflow_cache(workflow_name)  # Invalidate cache on update
            cache_workflow(workflow)
        return Workflow
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error updating workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to update workflow"}

def delete_workflow(db: Session, workflow_name: str):
    try:
        workflow = db.query(Workflow).filter(Workflow.name == workflow_name).first()
        if workflow:
            db.delete(workflow)
            db.commit()
            invalidate_workflow_cache(workflow_name)  # Invalidate cache on delete
        return {"message": "Workflow deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error deleting workflow {workflow_name}: {str(e)}")
        return {"error": "Failed to delete workflow"}

def list_workflows(db: Session):
    try:
        return db.query(Workflow).all()
    except SQLAlchemyError as e:
        logger.error(f"Error listing workflows: {str(e)}")
        return {"error": "Failed to list workflows"}