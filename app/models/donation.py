from sqlalchemy import (
    Column, Text,
    Integer, ForeignKey
)

from .abstract import Abstract


class Donation(Abstract):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
