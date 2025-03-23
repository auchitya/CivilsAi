from fastapi import FastAPI
from utils.postgress_conn import Base, db_instance
from apis import workflows, tasks

app = FastAPI(title="Workflow Automation API")

# Initialize database
Base.metadata.create_all(bind=db_instance.engine)

# Include routers
app.include_router(workflows.router)
app.include_router(tasks.router)
