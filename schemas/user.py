from pydantic import BaseModel
from typing import List


class AudioCollectionCreate(BaseModel):
    artist: str
    audio_format: str
    album: str
    year: int
    grade: str


class AudioCollection(AudioCollectionCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    nickname: str
    email: str
    hashed_password: str


class User(UserCreate):
    id: int
    is_active: bool
    collection: List[AudioCollection] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
