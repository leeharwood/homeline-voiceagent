import logging
import sys

def setup_logging():
    # Structured-like string formatting that is easy to parse, 
    # but still readable for local development.
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # You could add a JSONFormatter here for production usage,
    # or rely on standard formatting.
    logger = logging.getLogger("homeline")
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logging()
