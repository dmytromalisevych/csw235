from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, RelationshipProperty
from datetime import datetime
from typing import List
from .database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    password_hash: Mapped[str] = Column(String)
    is_active: Mapped[bool] = Column(Boolean, default=True)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    polls: Mapped[List["Poll"]] = relationship("Poll", back_populates="creator")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="user")

class Poll(Base):
    __tablename__ = "polls"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class PollOption(Base):
    __tablename__ = "poll_options"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    poll_id: Mapped[int] = Column(Integer, ForeignKey("polls.id", ondelete="CASCADE"))
    text: Mapped[str] = Column(String)

    poll: Mapped["Poll"] = relationship("Poll", back_populates="options")
    votes: Mapped[List["Vote"]] = relationship("Vote", back_populates="option")

class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    poll_id: Mapped[int] = Column(Integer, ForeignKey("polls.id"))
    option_id: Mapped[int] = Column(Integer, ForeignKey("poll_options.id"))
    voted_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="votes")
    poll: Mapped["Poll"] = relationship("Poll", back_populates="votes")
    option: Mapped["PollOption"] = relationship("PollOption", back_populates="votes")

    __table_args__ = (
        UniqueConstraint('user_id', 'poll_id', 'option_id', name='unique_vote'),
    )