from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Type

from models.participant import Participant
from dependencies import get_db
from schemas.participant import ParticipantCreate


class ParticipantRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self, group_id: int):
        query = self.db.query(Participant).filter(Participant.group == group_id)
        return query.all()

    def create(self, participant: ParticipantCreate):
        db_part = Participant(id=participant.id, name=participant.name, wish=participant.wish, group=participant.group_id)
        self.db.add(db_part)
        self.db.commit()
        self.db.refresh(db_part)

        return db_part.id

    def id(self):
        res = self.db.query(func.max(Participant.id)).first()
        return res[0]
    
    def get(self, participant_id: int):
        query = self.db.query(Participant).filter(Participant.id == participant_id)
        return query.first()
    
    def delete(self, participant_id: int):
        self.db.query(Participant).filter(Participant.id == participant_id).delete()
        self.db.commit()

    def update(self, participant_id: int, recipient_id: int):
        self.db.query(Participant).filter(Participant.id == participant_id).update({"recipient": recipient_id})
        self.db.commit()