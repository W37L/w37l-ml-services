from dependency_injector import providers, containers

from src.service.service_impl import MachineLearningService
from src.adapters.repository_impl import (
    MachineLearningRepository,
)


class ApplicationContainer(containers.DeclarativeContainer):
    configuration = providers.Configuration()

    machine_learning_repository = providers.Singleton(
        MachineLearningRepository, storage_dir=configuration.storage_dir
    )

    machine_learning_service = providers.Factory(MachineLearningService, machine_learning_repository)
