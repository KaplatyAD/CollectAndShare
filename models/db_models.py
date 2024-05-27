from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, Mapped


class UserDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    collection = relationship('AudioCollectionDB', back_populates='owner')

    def __repr__(self):
        return f'<UserDB(id={self.id}, nickname={self.nickname}, email={self.email}, is_active={self.is_active}, collection={self.collection})>'


class AudioCollectionDB(Base):
    __tablename__ = 'audio_collection'

    id = Column(Integer, primary_key=True)
    artist = Column(String)
    audio_format = Column(String)
    album = Column(String)
    year = Column(Integer)
    grade = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('UserDB', back_populates='collection')
