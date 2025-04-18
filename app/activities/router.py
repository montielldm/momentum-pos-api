from fastapi import APIRouter, Depends
from app.auth.utils import get_current_user

from app.activities.services import (
    get_all_tickets_service
)

activities = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)