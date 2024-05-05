from fastapi import APIRouter, HTTPException
from dependency_injector.wiring import Provide
from fastapi.responses import JSONResponse

from src.mlservice.service.service import IMachineLearningService
from src.mlservice.container import ApplicationContainer
from src.mlservice.model.model import *


machine_learning_service: IMachineLearningService = Provide(ApplicationContainer.machine_learning_service)

router = APIRouter(
    prefix="/MLService",
    tags=["MLService"],
    responses={404: {"description": "Not as found"}},
)

@router.post("/checkProfanity", response_model=Response)
async def check_profanity(text: str) -> JSONResponse:
    try:
        return machine_learning_service.check_profanity(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getHashtag", response_model=Response)
async def get_hashtag(text: str) -> JSONResponse:
    try:
        return machine_learning_service.get_hashtag(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  

@router.get("/getTrendingTopics", response_model=Response)
async def get_trending_topics() -> JSONResponse:
    try:
        return machine_learning_service.get_trending_topics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recomendationUser", response_model=list[User])
async def recommendation_user() -> JSONResponse:
    try:
        return machine_learning_service.get_recommendation_user()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recomendationPost", response_model=list[Post])
async def recommendation_post() -> JSONResponse:
    try:
        return machine_learning_service.get_recommendation_post()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))