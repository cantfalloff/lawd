from .config import database_url
from .db import db_manager
from .models import User, Tag, Session


db_manager.init(
    database_url,
    echo=False,
)
