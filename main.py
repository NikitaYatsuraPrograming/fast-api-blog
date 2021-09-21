from typing import List
import uvicorn
from fastapi import FastAPI
from app.api.routers import router as api_router

from app.db.database import Base
from app.db.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
