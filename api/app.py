from fastapi import Depends, FastAPI, Header, HTTPException
import uvicorn
from starlette.middleware.cors import CORSMiddleware
import api
from api import endpoints
from api.config import get_logger


_logger = get_logger(logger_name=__name__)

async def get_token_header(x_token: str=Header(...)):
    """
    This code block is taken from FastAPI's tutorial. NFI what it does

    Args:
        x_token: header information
    """
    if x_token != 'fake-super-secret-token':
        raise HTTPException(status_code=400, detail="X-Token header invalid")

def create_app(*, config_object) -> FastAPI:
    """
    Creates a FastAPI app to be used
    """
    _logger.info(f"[INFO]: Endpoint Version {api.__version__}")
    _logger.info(f"[INFO]: config_object is {config_object}")
    config = dict({"title": "De Dash API",
                   "description": "Initial release of De Dash API",
                   "version": api.__version__})

    app = FastAPI(title=config["title"],
                  description=config["description"],
                  version=config["version"])

    # Import endpoint API Routers are stored in endpoints.py
    app.include_router(api.endpoints.router)

    # Fucking CORS
    app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"])

    return app
