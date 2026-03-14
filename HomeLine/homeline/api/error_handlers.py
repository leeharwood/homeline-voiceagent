from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from homeline.utils.logging import logger
import traceback

def add_error_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception during {request.method} {request.url.path}: {exc}")
        logger.error(traceback.format_exc())
        
        # We always want Voice assistant to gracefully fail rather than read a literal 500 error struct
        return JSONResponse(
            status_code=200, # Returning 200 so the tool doesn't crash the conversation, but TTS states the error.
            content={"response": "I'm sorry, I encountered an internal error processing that request."}
        )
