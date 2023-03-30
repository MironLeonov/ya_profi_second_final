from sqlalchemy import Column, String, Integer, ForeignKey

from database import Model


class Participant(Model):
    __tablename__ = "participant"

    id = Column(Integer, primary_key=True,  default=int)
    name = Column(String)
    wish = Column(String)
    group = Column(Integer, ForeignKey("group.id", ondelete='CASCADE'))
    recipient = Column(Integer)
