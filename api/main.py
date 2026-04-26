"""FastAPI application entrypoint for production API routes."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import ALLOWED_ORIGINS
from .config import API_NAME
from .config import API_VERSION
from .config import ensure_runtime_directories
from .config import validate_security_configuration
from .middleware import RequestIdMiddleware
from .routers.auth import router as auth_router
from .routers.health import router as health_router
from .routers.search import router as search_router
from .routers.uploads import router as upload_router

ensure_runtime_directories()
validate_security_configuration()

app = FastAPI(
    title=API_NAME,
    version=API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(search_router)
app.include_router(upload_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Return a consistent response shape for validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "detail": "Validation error",
            "requestId": request_id,
            "errors": exc.errors(),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(
    request: Request,
    exc: Exception,  # pylint: disable=unused-argument
) -> JSONResponse:
    """Return sanitized internal error responses with request correlation."""
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "requestId": request_id,
        },
    )
