from fastapi import APIRouter,HTTPException
from database.book_db import BookDB
from database.member_db import MemberDB
from pydantic import BaseModel
from typing import Literal
import logging

logger = logging.getLogger(__name__)
book_router=APIRouter()

class CreateBook(BaseModel):
    title:str
    author:str
    genre:Literal["Fiction","Non-Fiction","Science","History","Other"]
    
class UpdateBook(BaseModel):
    title:str | None=None
    author:str | None=None
    genre:Literal["Fiction","Non-Fiction","Science","History","Other"] | None=None
    

@book_router.post("")
def create_book(data:CreateBook):
    logger.info(f"create new book {data.model_dump()}")
    book_db=BookDB()
    row=book_db.create_book(data.model_dump())
    print(data.model_dump())
    book_db.close_db()
    logger.info("the book created")
    if row: return {"message": 'book created in success'}
    else: return {"message":"something happend and book doeset created"}
    
@book_router.get("")
def get_all():
    logger.info("get all books")
    book_db=BookDB()
    data= book_db.get_all_books()
    book_db.close_db()
    return data

@book_router.get("/{id}")
def get_by_id(id):
    logger.info(f"get by id: {id}")
    book_db=BookDB()
    data = book_db.get_book_by_id(id)
    book_db.close_db()
    if not data:
        raise HTTPException(status_code=404,detail="Book not found")
    return data

@book_router.put("/{id}")
def update_book(id,data:UpdateBook):
    logger.info(f"update id: {id}")
    book_db=BookDB()
    changed = book_db.update_book(id,data.model_dump(exclude_none=True))
    book_db.close_db()
    if changed:
        logger.info("update book succeed")
        return {"message": "updating succeed"}
    else:
        logger.info("Update failed")
        return {"message": "updating failed"}


@book_router.put("/{id}/borrow/{member_id}")
def borrow_book(id,member_id):
    logger.info(f"borrow book: {id} by {member_id}")
    book_db=BookDB()
    member_db=MemberDB()
    
    book=book_db.get_book_by_id(id)
    member=member_db.get_member_by_id(member_id)
    
    if not book:
        logger.warning("Book not found")
        raise HTTPException(status_code=404,detail="Book not found")
    if not member:
        logger.warning("Member not found")
        raise HTTPException(status_code=404,detail="Member not found")
    if not book[4]:
        logger.warning("Book is not available")
        raise HTTPException(status_code=400,detail="Book is not available")
    if not member[3]:
        logger.warning("Member is not active")
        raise HTTPException(status_code=400,detail="Member is not active")
    if book_db.count_active_borrows_by_member(member_id)>=3:
        logger.warning("Member has reached maximum borrows")
        raise HTTPException(status_code=400,detail="Member has reached maximum borrows")
    member_db.increment_borrows(member_id)
    book_db.set_available(id,"borrow",member_id)
    book_db.close_db()
    member_db.close_db()
    logger.info(("the borrow succeed"))
    return {"message":"The borrow succeed"}

@book_router.put("/{id}/return/{member_id}")
def return_book(id,member_id):
    logger.info(f"return book {id} by {member_id}")
    book_db=BookDB()
    member_db=MemberDB()
    
    book=book_db.get_book_by_id(id)
    member=member_db.get_member_by_id(member_id)
    if not book:
        logger.warning("Book not found")
        raise HTTPException(status_code=404,detail="Book not found")
    if not member:
        logger.warning("Member not found")
        raise HTTPException(status_code=404,detail="Member not found")
    if book[4]:
        logger.warning("Book is not borrowed")
        raise HTTPException(status_code=400,detail="Book is not borrowed")
    if int(book[5]) != int(member_id):
        logger.warning("Book is not borrowed by this member")
        raise HTTPException(status_code=400, detail="Book is not borrowed by this member")
    
    book_db.set_available(id,"return",member_id)
    book_db.close_db()
    member_db.close_db()
    logger.info("the return succeed")
    return {"message":"The return succeed"}