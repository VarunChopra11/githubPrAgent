from fastapi import FastAPI
from app.routers import router
import uvicorn

app = FastAPI()

app.include_router(router.router)

@app.get("/")
async def default_root():
    return {"message": "Use /docs to see the API documentation."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)