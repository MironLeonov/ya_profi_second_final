from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Type

from models.group import Group
from dependencies import get_db
from schemas.group import GroupCreate


class GroupRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def all(self) -> List[Group]:
        query = self.db.query(Group)
        return query.all()

    def create(self, group: GroupCreate):
        db_group = Group(id=group.id, name=group.name, description=group.description)
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)

        return db_group.id

    def id(self):
        res = self.db.query(func.max(Group.id)).first()
        return res[0]

    def update(self, group: GroupCreate):
        self.db.query(Group).filter(Group.id == group.id).update({"name": group.name, "description": group.description})
        self.db.commit()

    def delete(self, group_id: int):
        self.db.query(Group).filter(Group.id == group_id).delete()
        self.db.commit()

    def get(self, group_id: int):
        query = self.db.query(Group).filter(Group.id == group_id)
        return query.first()