import redis
from celery import Celery
from app.config import Config
from app.services.agent_service import generate_response_from_agent
from app.services.github_service import get_pr_changes

celery_app = Celery("tasks", broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)


@celery_app.task(bind=True)
def start_task(self, data: dict, *args, **kwargs):
    print("Data received in task:", data)
    task_id = self.request.id

    redis_client.hset(task_id, mapping={"status": "processing"})
    # redis_client.set(task_id, mapping={"status": "processing"})

    pr_changes = get_pr_changes(data["repo_url"], data["pr_number"], data["github_token"])
    result = generate_response_from_agent(pr_changes)

    if result["status"] == "success":
        redis_client.hset(task_id, "task_id", task_id)
        redis_client.hset(task_id, "status", "completed")
        redis_client.hset(task_id, "response", result["response"])
        
    else:
        redis_client.hset(task_id, "status", "failed")
        redis_client.hset(task_id, "error", result["message"])
        redis_client.hset(task_id, "task_id", task_id)

    return task_id
