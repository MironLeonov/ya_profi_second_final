from sqlalchemy import Column, String, Integer, Identity

from database import Model


class Group(Model):
    __tablename__ = "group"

    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True, default=int)
    name = Column(String)
    description = Column(String, nullable=True)
