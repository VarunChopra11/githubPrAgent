from pydantic import BaseModel, Field

class InputModel(BaseModel):
    repo_url: str  # Enforces URL validation
    pr_number: int = Field(..., gt=0, description="Pull request number must be greater than 0")
    github_token: str = Field(None, description="Optional GitHub token for authentication")