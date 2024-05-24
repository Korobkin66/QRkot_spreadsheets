from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class CharityProjectsBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)


class CharityProjectCreate(CharityProjectsBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...)


class CharityProjectUpdate(CharityProjectsBase):

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
