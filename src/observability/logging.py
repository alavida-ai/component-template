import logging
import os
import sys

import structlog


def setup_logging():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level, logging.INFO)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


setup_logging()


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
