LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "simple": {
            "format": "[%(levelname)s] %(name)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s %(funcName)s():%(lineno)d: %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "simple"
        },
        "db_fh": {
            "class": "logging.FileHandler",
            "filename": f"logs/db.log",
            "level": "DEBUG",
            "formatter": "detailed"
        },
    },

    "loggers": {
        "database": {
            "level": "DEBUG",
            "handlers": ["console", "db_fh"],
            "propagate": False
        },
    }
}
