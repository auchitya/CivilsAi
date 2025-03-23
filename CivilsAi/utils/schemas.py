from pydantic import BaseModel
from typing import List, Optional
import enum

class ExecutionType(str, enum.Enum):
    SYNC = "sync"
    ASYNC = "async"

# Workflow Schemas
class WorkflowBase(BaseModel):
    name: str

class WorkflowCreate(WorkflowBase):
    pass
    # tasks: Optional[List["TaskCreate"]] = None

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    # tasks: Optional[List["TaskCreate"]] = None

class WorkflowResponse(WorkflowBase):
    name: str
    status: str

    class Config:
        orm_mode = True

class WorkflowTasksResponse(WorkflowBase):
    name: str
    status: str
    tasks: List["TaskResponse"]

    class Config:
        orm_mode = True

# Task Schemas
class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    execution_type: ExecutionType

class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    order: int
    execution_type: ExecutionType

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    execution_type: Optional[ExecutionType] = None

class TaskResponse(TaskBase):
    name: str
    description: Optional[str] = None
    order: int
    execution_type: ExecutionType

    class Config:
        orm_mode = True


WorkflowTasksResponse.update_forward_refs()