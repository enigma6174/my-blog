from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from app.database import Base


class FastapiVoting(Base):
    __tablename__ = "blog_votes"
    user_id = Column(Integer, ForeignKey("fastapi_users.uid", ondelete="CASCADE"), primary_key=True)
    blog_id = Column(Integer, ForeignKey("fastapi_blog_post.bid", ondelete="CASCADE"), primary_key=True)
