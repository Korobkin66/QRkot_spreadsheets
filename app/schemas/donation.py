from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    full_amount: PositiveInt
    create_date: datetime
    id: int

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = Field(0)
    fully_invested: bool
    close_date: Optional[datetime]


class DonationMY(DonationCreate):
    id: int
    create_date: datetime
