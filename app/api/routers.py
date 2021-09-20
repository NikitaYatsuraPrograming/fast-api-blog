from fastapi import APIRouter
from app.api.authorization import api as authorization
from app.api.item import api as items

router = APIRouter()
router.include_router(authorization.router, tags=["authentication"], prefix="/users")
router.include_router(items.router, tags=["item"], prefix="/items")