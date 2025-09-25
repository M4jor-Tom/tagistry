from logging.config import dictConfig


def setup_logging(log_level: str) -> None:
    """Set up logging configuration for the entire application."""
    dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "core": {
                "level": log_level,
                "handlers": [],
                "propagate": False,
            },
        },
    })
