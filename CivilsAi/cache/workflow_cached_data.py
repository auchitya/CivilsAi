import json
from models.sql_models import Workflow
from utils.postgress_conn import redis_client


CACHE_EXPIRATION = 60 * 5  # Cache for 5 minutes

def get_cached_workflow(workflow_name: str):
    cached_workflow = redis_client.get(f"workflow:{workflow_name}")
    return json.loads(cached_workflow) if cached_workflow else None

def cache_workflow(workflow: Workflow):
    redis_client.setex(
        f"workflow:{workflow.name}", CACHE_EXPIRATION, json.dumps({
            "status": workflow.status.value
        })
    )

def invalidate_workflow_cache(workflow_name: str):
    redis_client.delete(f"workflow:{workflow_name}")