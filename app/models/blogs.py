from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.database import Base


class FastapiBlogPost(Base):
    __tablename__ = "fastapi_blog_post"

    bid = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    rating = Column(Integer, nullable=True, server_default='0')
    is_published = Column(Boolean, nullable=True, server_default='FALSE')
    inserted_dt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
