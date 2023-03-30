from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import PlainTextResponse

from schemas.participant import ParticipantBase, ParticipantCreate
from repositories.participant import ParticipantRepository

router = APIRouter(prefix="/group", tags=["participant"])


@router.post("/{group_id}/participant", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
def store_participant(group_id: int, participant: ParticipantBase, participants: ParticipantRepository = Depends()):
    try:
        new_part_id = participants.id() + 1
    except TypeError:
        new_part_id = 0
    db_part = ParticipantCreate(id=new_part_id, name=participant.name, wish=participant.wish, group_id=group_id)
    db_id = participants.create(db_part)
    return PlainTextResponse(content=str(db_id), status_code=status.HTTP_201_CREATED)


@router.delete("/{group_id}/participant/{part_id}", status_code=status.HTTP_200_OK)
def delete_participant(group_id: int, part_id: int, participants: ParticipantRepository = Depends()):
    participants.delete(part_id)

@router.get("/{group_id}/participant/{part_id}/recipient", status_code=status.HTTP_200_OK)
def get_recipient(group_id: int, part_id: int, participants: ParticipantRepository = Depends()):
    participant = participants.get(part_id)
    if participant:
        recipient = participants.get(participant.recipient)

        return {"id": recipient.id, "name": recipient.name, "wish":  recipient.wish}
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)