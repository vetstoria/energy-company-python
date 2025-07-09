from http import HTTPStatus
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from .app_initializer import initialize_data
from .db import create_tables, database
from .router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup phase
    create_tables()
    await database.connect()
    await initialize_data()

    yield  # ⬅ app runs while suspended here

    # Shutdown phase
    await database.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(title="EnergyCompany (MySQL)", lifespan=lifespan)

    # --------------------------------------------------------------------- #
    # Routers & error handling                                              #
    # --------------------------------------------------------------------- #
    app.include_router(api_router)

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(request, exc):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.warning(f"{request}: {exc_str}")
        content = {"message": exc_str, "data": None}
        return JSONResponse(
            content=content, status_code=HTTPStatus.UNPROCESSABLE_ENTITY
        )

    return app


app = create_app()