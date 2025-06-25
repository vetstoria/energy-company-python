from http import HTTPStatus

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.responses import JSONResponse

from .app_initializer import initialize_data
from .db import create_tables, database
from .router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="EnergyCompany (MySQL)")

    # --------------------------------------------------------------------- #
    # Lifespan events                                                       #
    # --------------------------------------------------------------------- #
    @app.on_event("startup")
    async def _startup() -> None:
        create_tables()  # idempotent DDL
        await database.connect()
        await initialize_data()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await database.disconnect()

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
