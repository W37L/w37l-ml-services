import os
from dependency_injector import providers, containers

from src.mlservice.service.service_impl import MachineLearningService
from src.mlservice.adapters.repository_impl import (
    MachineLearningRepository, MockMachineLearningRepository
)


class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    use_mock_repository = os.getenv("USE_MOCK_REPOSITORY", False)

    machine_learning_repository = providers.Factory(
        lambda: MockMachineLearningRepository() if ApplicationContainer.use_mock_repository else MachineLearningRepository(storage_dir=ApplicationContainer.configuration.storage_dir),
    )

    machine_learning_service = providers.Factory(
        MachineLearningService, ml_repository=machine_learning_repository
    )
