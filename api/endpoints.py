from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

@router.get('/')
async def root():
    """ Root URL, for version checking. """
    # TODO: Remove this endpoint when health and version is setup.
    return f"DeDash Restful API, version 0.0.1"

@router.get('/health')
async def health():
    """
    Health check endpoint. Allows users to check the health of the API with
    a get request to this endpoint.
    """
    # TODO: What is the name of this app!?!?!
    return f"DeDash RESTful API, Version 0.0.1"

@router.post('/user')
async def user(*, username:str):
    raise NotImplementedError

@router.post('/story')
async def story(*, story:int):
    raise NotImplementedError
