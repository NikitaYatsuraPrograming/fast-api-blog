from typing import List
import uvicorn
from fastapi import FastAPI
from app.api.routers import router as api_router


app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
