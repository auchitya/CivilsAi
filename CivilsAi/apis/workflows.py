from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.postgress_conn import db_instance
from utils import schemas
from crud import workflow_crud as crud

router = APIRouter(prefix="/workflows", tags=["Workflows"])

def get_db():
    return next(db_instance.get_db())

@router.post("/", response_model=schemas.WorkflowResponse)
def create_workflow(workflow: schemas.WorkflowCreate, db: Session = Depends(get_db)):
    return crud.create_workflow(db, workflow)

@router.get("/{workflow_name}", response_model=schemas.WorkflowTasksResponse)
def get_workflow(workflow_name: str, db: Session = Depends(get_db)):
    workflow = crud.get_workflow(db, workflow_name)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.get("/", response_model=list[schemas.WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)):
    return crud.list_workflows(db)

@router.put("/{workflow_name}", response_model=schemas.WorkflowResponse)
def update_workflow(workflow_name: str, workflow: schemas.WorkflowUpdate, db: Session = Depends(get_db)):
    updated_workflow = crud.update_workflow(db, workflow_name, workflow)
    if not updated_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return updated_workflow

@router.delete("/{workflow_name}")
def delete_workflow(workflow_name: str, db: Session = Depends(get_db)):
    deleted_workflow = crud.delete_workflow(db, workflow_name)
    if not deleted_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return delete_workflow
