from fastapi import APIRouter, Depends, status, Response
from pydantic import parse_obj_as
from fastapi.responses import PlainTextResponse
from typing import List

from schemas.group import GroupBase, GroupCreate
from repositories.group import GroupRepository
from repositories.participant import ParticipantRepository
import random

router = APIRouter(tags=["group"])


@router.get("/groups", response_model=List[GroupCreate])
def list_groups(group: GroupRepository = Depends()):
    db_groups = group.all()
    return parse_obj_as(List[GroupCreate], db_groups)


@router.post("/group", response_class=PlainTextResponse, status_code=status.HTTP_201_CREATED)
def store_group(group: GroupBase, groups: GroupRepository = Depends()):
    try:
        new_group_id = groups.id() + 1
    except TypeError:
        new_group_id = 0
    db_group = GroupCreate(id=new_group_id, name=group.name, description=group.description)
    db_id = groups.create(db_group)
    return PlainTextResponse(content=str(db_id), status_code=status.HTTP_201_CREATED)


@router.put("/group/{group_id}", status_code=status.HTTP_200_OK)
def update_group(group_id: int, group: GroupBase, groups: GroupRepository = Depends()):
    db_group = GroupCreate(id=group_id, name=group.name, description=group.description)
    groups.update(db_group)


@router.delete("/group/{group_id}", status_code=status.HTTP_200_OK)
def delete_group(group_id: int, groups: GroupRepository = Depends()):
    groups.delete(group_id)


@router.get("/group/{group_id}", status_code=status.HTTP_200_OK)
def get_group(group_id: int, groups: GroupRepository = Depends(), participants: ParticipantRepository = Depends()):
    cur_group = groups.get(group_id)
    if cur_group:
        cur_parts = participants.all(group_id)

        res = dict()
        res['id'] = group_id
        res['name'] = cur_group.name
        res['description'] = cur_group.description

        parts = list()
        for part in cur_parts:
            if part.recipient:
                recip = participants.get(part.recipient)
                if recip:
                    parts.append({"id": part.id, "name": part.name, "wish": part.wish, "recipient": {'id': recip.id, 'name': recip.name, 'wish': recip.wish}})
                else: 
                    parts.append({"id": part.id, "name": part.name, "wish": part.wish, "recipient": {}})
            else: 
                parts.append({"id": part.id, "name": part.name, "wish": part.wish, "recipient": {}})


        res['participants'] = parts

        return res
    else: 
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/group/{group_id}/toss", status_code=status.HTTP_200_OK)
def toss(group_id: int, participants: ParticipantRepository = Depends()):
    
    cur_part = participants.all(group_id)
    if cur_part:
        if len(cur_part) >= 3: 

            res = []
            part_ids = []
            for part in cur_part: 
                part_ids.append(part.id)
                res.append({'id': part.id, 'name': part.name, 'wish': part.wish})
            is_used = set()
            part_recip = {}

            recip_id = random.choice(part_ids)
            for part_id in part_ids: 
                if recip_id == part_id or recip_id in is_used:
                    while recip_id == part_id or recip_id in is_used:
                        recip_id = random.choice(part_ids)
                part_recip[part_id] = recip_id
                is_used.add(recip_id)

            for part_id, recip_id in part_recip.items(): 
                participants.update(part_id, recip_id)
            
            for part in res: 
                recip_id = part_recip[part['id']]
                recip = participants.get(recip_id)
                part['recipient'] = {'id': recip.id, 'name': recip.name, 'wish': recip.wish}

            return res
        else: 
            return Response(status_code=status.HTTP_409_CONFLICT)
    else: 
        return Response(status_code=status.HTTP_404_NOT_FOUND)
