from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.log import get_logger, setup_logging
from app.routers import health, type1, type2, unified
from app.schemas.api import ErrorResponse


def create_app() -> FastAPI:
    setup_logging(get_settings().log_level)
    log = get_logger(__name__)

    app = FastAPI(
        title="EXACT 2026 — XAI Educational QA",
        version="0.1.0",
        description="Logic + physics QA with explainable answers.",
    )

    log.info("[bold green]FastAPI app initialized[/bold green] model=%s", get_settings().model_name)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        log.exception("Unhandled error on %s", request.url.path)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(detail=str(exc), code="internal_error").model_dump(),
        )

    app.include_router(health.router)
    app.include_router(type1.router)
    app.include_router(type2.router)
    app.include_router(unified.router)
    return app


app = create_app()
