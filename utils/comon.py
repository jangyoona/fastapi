from fastapi import HTTPException
from core.config import ALLOWED_HOST
import logging

logger = logging.getLogger(__name__)

def is_allowed_host(host: str) -> bool:
    logger.info("request_host=%s", host)
    return ALLOWED_HOST == host