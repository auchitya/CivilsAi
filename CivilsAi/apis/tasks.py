from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.postgress_conn import db_instance
from utils import schemas
from crud import task_crud as crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])

def get_db():
    return next(db_instance.get_db())

@router.post("/{workflow_name}", response_model=schemas.TaskResponse)
def add_task(workflow_name: str, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = crud.add_task_to_workflow(db, workflow_name, task)
    if not new_task:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return new_task

@router.put("/{workflow_name}/{task_name}", response_model=schemas.TaskResponse)
def update_task(workflow_name: str, task_name: str, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, workflow_name, task_name, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found in the specified workflow")
    return updated_task

@router.delete("/{workflow_name}/{task_name}")
def delete_task(workflow_name: str, task_name: str, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, workflow_name, task_name)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found in the specified workflow")
    return delete_task




