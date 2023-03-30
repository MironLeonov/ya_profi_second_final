from pydantic import BaseModel


class GroupBase(BaseModel):
    name: str
    description: str = None

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    id: int

