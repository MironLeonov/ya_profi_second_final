from pydantic import BaseModel


class ParticipantBase(BaseModel):
    name: str
    wish: str = None

    class Config:
        orm_mode = True


class ParticipantCreate(ParticipantBase):
    id: int
    group_id: int



