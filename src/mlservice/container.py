from dependency_injector import providers, containers

from src.mlservice.service.service_impl import MachineLearningService
from src.mlservice.adapters.repository_impl import (
    MachineLearningRepository, MockMachineLearningRepository
)


class ApplicationContainer(containers.DeclarativeContainer):
    """
    Dependency injection container for the Machine Learning Service application.

    This container manages the creation and injection of dependencies required by the
    Machine Learning Service application. It provides access to configuration, 
    machine learning repository (either mock or actual), and the machine learning service itself.
    """

    configuration = providers.Configuration()
    """
    This provider retrieves configuration settings from the configured source.
    """

    use_mock_repository = True
    """
    Boolean flag indicating whether to use a mock repository.
    """

    machine_learning_repository = providers.Factory(
        lambda: MockMachineLearningRepository() if ApplicationContainer.use_mock_repository else MachineLearningRepository(storage_dir=ApplicationContainer.configuration.storage_dir),
    )
    """
    This factory function dynamically creates the appropriate machine learning repository
    based on the `use_mock_repository` flag. It utilizes the configuration provider
    (`configuration`) to access the storage directory for the actual repository.
    """

    machine_learning_service = providers.Factory(
        MachineLearningService, ml_repository=machine_learning_repository
    )
    """
    Provider for the machine learning service.

    This factory function creates an instance of the `MachineLearningService` class.
    It injects the `machine_learning_repository` dependency, ensuring 
    the service has access to the underlying repository for data access.
    """