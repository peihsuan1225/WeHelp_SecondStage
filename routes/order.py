from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from pydantic import BaseModel
import json

from .config import connection_pool
from .utils import get_current_user

router = APIRouter()