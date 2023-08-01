from datetime import datetime

from asyncpg import UniqueViolationError

from db.db_connection import db
from db.schemas.tables import User, Payment



