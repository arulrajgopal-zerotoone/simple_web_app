from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    user_id: int
    username: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RecordCreate(BaseModel):
    topic: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None


class RecordUpdate(BaseModel):
    topic: Optional[str] = None
    description: Optional[str] = None


class RecordOut(BaseModel):
    record_id: int
    topic: str
    description: Optional[str]
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
