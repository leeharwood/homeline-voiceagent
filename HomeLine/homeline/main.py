from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from homeline.db.database import init_db
from homeline.api.routes import api_router
from homeline.api.error_handlers import add_error_handlers
from homeline.utils.logging import logger

def create_app() -> FastAPI:
    logger.info("Starting up HomeLine Real Estate AI Assistant API")

    app = FastAPI(
        title="HomeLine Real Estate AI Assistant API",
        description="Production Backend for Telnyx AI Assistant real estate MVP",
        version="2.0.0"
    )

    # Database Initialization
    init_db()

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(api_router, prefix="/api")

    # Error Handlers
    add_error_handlers(app)

    return app

app = create_app()
