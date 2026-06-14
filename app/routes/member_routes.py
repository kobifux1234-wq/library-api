from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from database.member_db import MemberDB
import logging

logger = logging.getLogger(__name__)

class CreateMember(BaseModel):
    name:str
    email:str
    total_borrows:int = 0

class UpdateMember(BaseModel):
    name:str|None=None
    email:str |None=None
member_router=APIRouter()

@member_router.post("")
def create_member(data:CreateMember):
    logger.info("start in creating new member")
    member_db=MemberDB()
    row = member_db.create_member(data.model_dump())
    member_db.close_db()
    if row:
        logger.info("Member created")
        return{"message":"Member created"}
    else: 
        logger.warning("Adding new member failed")
        return {"message":"Adding new member failed"}
    
@member_router.get("")
def all_members():
    logger.info("get all members")
    member_db=MemberDB()
    data= member_db.get_all_members()
    member_db.close_db()
    return data


@member_router.get("/{id}")
def member_by_id(id):
    logger.info(f"get by id: {id}")
    member_bd=MemberDB()
    data= member_bd.get_member_by_id(id)
    member_bd.close_db()
    if not data:
        logger.warning(f"member not found: {id}")
        raise HTTPException(status_code=404,detail="Member not found")
    logger.info(f"get member id: {id}")
    return data
    
@member_router.put("/{id}")
def update_member(id,data:UpdateMember):
    logger.info(f"updating id: {id}")
    member_bd=MemberDB()
    changed=member_bd.update_member(id,data.model_dump(exclude_none=True))
    member_bd.close_db()
    if changed:
        logger.info("update member succeed")
        return {"message": "updating succeed"}
    else:
        logger.warning("update member failed") 
        return {"message": "updating failed"}

@member_router.patch("/{id}/deactivate")
def deactivate_member(id):
    logger.info(f"deactivate id: {id}")
    member_bd=MemberDB()
    changed=member_bd.deactivate_member(id)
    member_bd.close_db()
    if not changed:
        logger.warning("deactivate member failed")
        return {"message":"Nothing happened"}
    logger.info("deactivate member succeed")
    return {"message": "deactivate succeed"}


@member_router.patch("/{id}/activate")
def deactivate_member(id):
    logger.info(f"activate id: {id}")
    member_bd=MemberDB()
    changed=member_bd.activate_member(id)
    member_bd.close_db()
    if not changed:
        logger.warning("Nothing changed in activate member")
        return {"message":"Nothing happened"}
    logger.info("activate member succeed")
    return {"message": "activate succeed"}