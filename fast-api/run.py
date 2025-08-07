#!/usr/bin/env python3
"""
Startup script for the FastAPI application
"""

import uvicorn

from config import settings
from main import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
