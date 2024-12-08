from fastapi import APIRouter, HTTPException
from app.models import InputModel
from app.tasks import start_task, redis_client
import json

router = APIRouter()

@router.post("/analyze-pr")
def analyze_pr(data: InputModel):
    """
    This endpoint will analyze the Pull Request. 
    - `github_token` is optional. If you don't provide it, it will be assumed that the provided repo url is public repository.
    - If you want to analyze a private repo provide the `github_token`.

    - You can use the following dummy data to test the endpoint:
        {
            "repo_url": "https://github.com/sharmavikas4/MERN_BLOG",
            "pr_number": 53
        }
    """
    print("Data passed to task:", data.model_dump())
    task_id = start_task.apply(kwargs={"data": data.model_dump()}).get()
    # print("Task ID: ", task.id)
    if not task_id:
        raise HTTPException(status_code=500, detail="Failed to start task.")
    return {"task_id": task_id, "status": "pending"}

@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    """
       - This endpoint will return the status of the task.
       - Use the task_id returned by the analyze-pr endpoint for status.
    """
    status = redis_client.hget(task_id, "status")
    if not status:
        raise HTTPException(status_code=404, detail="Task ID not found.")
    return {"task_id": task_id, "status": status}

@router.get("/results/{task_id}")
def get_task_result(task_id: str):
    """
       - This endpoint will return the results of the task.
       - Use the task_id returned by the analyze-pr endpoint for results.
    """
    task_data = redis_client.hgetall(task_id)
    task_data["response"] = json.loads(task_data["response"])
    if not task_data:
        raise HTTPException(status_code=404, detail="Task ID not found.")
    return task_data
