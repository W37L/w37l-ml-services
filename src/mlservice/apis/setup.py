from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.mlservice.container import ApplicationContainer
from src.mlservice.apis import controller


def setup(app: FastAPI, container: ApplicationContainer) -> None:

    app.include_router(controller.router)

    # Inject dependencies
    container.wire(
        modules=[
            controller,
        ]
    )

    # Customize the openAPI documentation
    def custom_openapi() -> Any:
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
