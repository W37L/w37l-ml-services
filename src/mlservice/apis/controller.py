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
    """
    Checks the provided text for profanity using the machine learning service.

    This endpoint takes a string of text as input and utilizes the injected 
    `machine_learning_service` to determine if the text contains profanity.

    Args:
        text (str): The text to be checked for profanity.

    Returns:
        JSONResponse: A JSON response containing the results of the profanity check.
        The specific format of the response depends on the implementation of the 
        `machine_learning_service`.

    Raises:
        HTTPException: If an error occurs during the profanity check, an HTTPException
        with status code 500 (Internal Server Error) and the error details will be raised.
    """
    try:
        return machine_learning_service.check_profanity(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getHashtag", response_model=Response)
async def get_hashtag(text: str) -> JSONResponse:
    """
    Generates hashtags for the provided text using the machine learning service.

    This endpoint takes a string of text as input and utilizes the injected 
    `machine_learning_service` to generate appropriate hashtags for the text.

    Args:
        text (str): The text for which hashtags should be generated.

    Returns:
        JSONResponse: A JSON response containing the generated hashtags.
        The specific format of the response depends on the implementation of the 
        `machine_learning_service`.
    """
    try:
        return machine_learning_service.get_hashtag(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  

@router.get("/getTrendingTopics", response_model=Response)
async def get_trending_topics() -> JSONResponse:
    """
    Retrieves the current trending topics using the machine learning service.

    This endpoint leverages the injected `machine_learning_service` to fetch 
    information about the current trending topics.

    Returns:
        JSONResponse: A JSON response containing the trending topics.
        The specific format of the response depends on the implementation of the 
        `machine_learning_service`.
    """
    try:
        return machine_learning_service.get_trending_topics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recomendationUser", response_model=Response)
async def recommendation_user(userId: str) -> JSONResponse:
    """
    Retrieves recommendations for users based on their preferences.

    Args:
        userId (str): The userId for which users recomendation should be generated.
    
    This endpoint returns a JSON response containing recommended user IDs.
    """

    try:
        # Call the machine learning service to get recommendations
        return machine_learning_service.get_recommendation_user(userId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recomendationPost", response_model=Response)
async def recommendation_post(userId: str) -> JSONResponse:
    """
    Retrieves recommendations for posts based on user preferences.
    
    Args:
        userId (str): The userId for which users recomendation should be generated.

    This endpoint returns a JSON response containing recommended post IDs.
    """

    try:
        # Call the machine learning service to get recommendations
        return machine_learning_service.get_recommendation_post(userId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))