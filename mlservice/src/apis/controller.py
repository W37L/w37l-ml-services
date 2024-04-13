from dependency_injector.wiring import Provide
from fastapi import APIRouter

from src.service.service import IMachineLearningService
from src.container import ApplicationContainer

machine_learning_service: IMachineLearningService = Provide[ApplicationContainer.machine_learning_service]

router = APIRouter(
    prefix="/MLService",
    tags=["MLService"],
    responses={404: {"description": "Not found"}},
)


@router.post("/checkProfanity", response_model=bool)
async def check_profanity(text: str) -> bool:
    return machine_learning_service.check_profanity(text)

@router.get("/getTrendingTopics", response_model=bool)
async def check_text() -> bool:
    return False

# recomendationUser method response model list string
@router.get("/recomendationUser", response_model=list[str])
async def recomendation_user() -> list[str]:
    return ["recomendationUser"]

# recomendationpost method response model list string
@router.get("/recomendationPost", response_model=list[str])
async def recomendation_post() -> list[str]:
    return ["recomendationPost"]


