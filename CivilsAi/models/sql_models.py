from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from utils.postgress_conn import Base
import enum

class ExecutionType(str, enum.Enum):
    SYNC = "sync"
    ASYNC = "async"

class WorkflowStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Workflow(Base):
    __tablename__ = "workflows"

    name = Column(String, primary_key=True, nullable=False, unique=True)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.PENDING)
    
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete")

class Task(Base):
    __tablename__ = "tasks"

    name = Column(String, primary_key=True, nullable=False)
    description = Column(String)
    order = Column(Integer, nullable=False)
    execution_type = Column(Enum(ExecutionType), nullable=False)
    workflow_name = Column(String, ForeignKey("workflows.name", ondelete="CASCADE"), nullable=False)

    workflow = relationship("Workflow", back_populates="tasks")
