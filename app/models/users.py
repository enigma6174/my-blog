from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base


class FastapiUsers(Base):
    __tablename__ = "fastapi_users"

    uid = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    inserted_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
