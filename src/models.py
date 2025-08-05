from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as pyenum

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False )
    firstname: Mapped[str] = mapped_column(String(20),unique=False, nullable=False )
    lastname: Mapped[str] = mapped_column(String(20),unique=False, nullable=False )
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post (db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(backref="posts")


class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)

    following_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    following: Mapped["User"] = relationship(backref = "following")

    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    follower: Mapped["User"] = relationship(backref = "follower")

    def serialize(self):
        return {
            "id": self.id,
            "following_id": self.following_id,
            "follower_id": self.follower_id
        }
    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    comment_text: Mapped[str] = mapped_column(String(160))

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(backref="author_name")

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(backref="authpor_post")

    def serialize(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
    
class MediaType(pyenum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    type: Mapped[pyenum] = mapped_column(Enum(MediaType))
    url: Mapped[str] = mapped_column(String(200))

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(backref="post")

    def serialize(self):
        return {
            "id": self.id,
            "post_id": self.post_id
        }