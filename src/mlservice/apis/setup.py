from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.mlservice.container import ApplicationContainer
from src.mlservice.apis import controller


def setup(app: FastAPI, container: ApplicationContainer) -> None:
    """
    Sets up the FastAPI application with routing, dependency injection, and OpenAPI customization.

    This function performs the following tasks:

    1. Includes the router defined in the `controller` module.
    2. Wires dependencies using the provided `container` object.
    3. Customizes the OpenAPI documentation for the API.

    Args:
        app (FastAPI): The FastAPI application instance.
        container (ApplicationContainer): The dependency injection container object.
    """

    app.include_router(controller.router)

    # Inject dependencies
    container.wire(
        modules=[
            controller,
        ]
    )

    # Customize the openAPI documentation
    def custom_openapi() -> Any:
        """
        Customizes the OpenAPI documentation for the API.

        This function defines a custom OpenAPI schema for the API, including:
         - Title: "ML Service API"
         - Version: "0.1"
         - Description: "Machine Learning Service API"
         - Routes: Information about the API routes
         - Server URL: Configured based on the API prefix from the container

        Returns:
            Any: The customized OpenAPI schema dictionary.
        """
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="ML Service API",
            version="0.1",
            description="Machine Learning Service API",
            routes=app.routes,
        )
        if not container.configuration.api_prefix():
            openapi_schema["servers"] = [{"url": "/"}]
        else:
            openapi_schema["servers"] = [{"url": container.configuration.api_prefix()}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi