import logging
from pathlib import Path
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, JSONResponse
import uvicorn

from src.mlservice.container import ApplicationContainer
from src.mlservice.apis.setup import setup
from src.mlservice import __version__

app = FastAPI(title="ML Service API")

# Add CORS middleware to allow connections from all origins
"""
Enables CORS (Cross-Origin Resource Sharing) for the API.

This middleware allows requests from any origin (`allow_origins=["*"]`). 
In a production environment, you'll likely want to restrict origins for security reasons.

It also allows all HTTP methods (`allow_methods=["*"]`), headers (`allow_headers=["*"]`),
and enables the use of credentials (`allow_credentials=True`).

"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", include_in_schema=False)
def root_redirect():
    """
    Redirects root path requests to API documentation.

    This function redirects any request to the root path (`/`) to the API documentation 
    located at `/docs`. This helps with discoverability and ease of use.
    """
    return RedirectResponse(url='/docs')

@app.on_event("startup")
async def startup_event():
    """
    This function is executed when the application starts. It performs the following tasks:

    1. Prints a message indicating the application is starting.
    2. Creates an instance of the `ApplicationContainer` class (likely used for dependency injection).
    3. Configures the logging level based on the environment variable "ML_Service_LOG_LEVEL".
    4. Configures the storage directory based on the environment variable "MLSERVICE_STORAGE_DIR".
    5. Calls the `setup` function (presumably for setting up routes and dependencies) using the container.
    """
    print("App is starting")
    container = ApplicationContainer()
    container.configuration.log_level.from_env("ML_Service_LOG_LEVEL", "INFO")
    str_level = container.configuration.log_level()
    numeric_level = getattr(logging, str_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {str_level}")
    logging.basicConfig(level=numeric_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Logging level is set to {str_level.upper()}")
    container.configuration.storage_dir.from_env("MLSERVICE_STORAGE_DIR", "/tmp/mlservice")
    Path(container.configuration.storage_dir()).mkdir(parents=True, exist_ok=True)
    setup(app, container)

@app.get("/status", tags=["Utility"])
def get_status():
    """
    Returns the status of the application.

    This endpoint provides a simple JSON response indicating the application is running
    and includes the current version information.
    """
    return JSONResponse(content={"status": "running", "version": __version__})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)