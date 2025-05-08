
# here, "fh" stands for "file hanlder"
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
        "root_fh": {
            "class": "logging.FileHandler",
            "filename": f"logs/root.log",
            "level": "DEBUG",
            "formatter": "detailed"
        },
        "db_fh": {
            "class": "logging.FileHandler",
            "filename": f"logs/db.log",
            "level": "DEBUG",
            "formatter": "detailed"
        },
        "api_fh": {
            "class": "logging.FileHandler",
            "filename": f"logs/api.log",
            "level": "DEBUG",
            "formatter": "detailed"
        },
    },

    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "root_fh"],
            "propagate": False
        },
        "database": {
            "level": "DEBUG",
            "handlers": ["console", "db_fh"],
            "propagate": False
        },
        "api": {
            "level": "DEBUG",
            "handlers": ["console", "api_fh"],
            "propagate": False
        },
    }
}
