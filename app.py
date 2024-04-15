import logging
from pathlib import Path

from fastapi import FastAPI
import uvicorn

from src.mlservice.container import ApplicationContainer
from src.mlservice.apis.setup import setup
from src.mlservice import __version__


def init() -> FastAPI:
    container = ApplicationContainer()

    # Setup logging
    container.configuration.log_level.from_env("ML_Service_LOG_LEVEL", "INFO")

    str_level = container.configuration.log_level()
    numeric_level = getattr(logging, str_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % str_level)
    logging.basicConfig(level=numeric_level)
    logger = logging.getLogger(__name__)
    logger.info("Logging level is set to %s" % str_level.upper())

    # init Database
    container.configuration.storage_dir.from_env("MLSERVICE_STORAGE_DIR", "/tmp/mlservice")
    Path(container.configuration.storage_dir()).mkdir(parents=True, exist_ok=True)

    # Init API and attach the container
    app = FastAPI()
    app.extra["container"] = container

    # Do setup and dependencies wiring
    setup(app, container)

    return app


def start() -> None:
    """Start application"""
    logger = logging.getLogger(__name__)
    logger.info(f"Machine Learning Service version: {__version__}")
    app = init()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":
    start()
