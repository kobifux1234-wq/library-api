from fastapi import APIRouter
from database.book_db import BookDB
from database.member_db import MemberDB

report_router=APIRouter()


@report_router.get("/summary")
def get_summary():
    book_data = BookDB()
    members_data = MemberDB()
    total_books = book_data.count_total_books()
    available_books= book_data.count_available_books()
    currently_borrowed=book_data.count_borrowed_books()
    active_members=members_data.count_active_members()
    book_data.close_db()
    members_data.close_db()
    return {
"total_books": total_books,
"available_books": available_books,
"currently_borrowed": currently_borrowed,
"active_members": active_members
}
    

@report_router.get("/books-by-genre")
def get_by_genre():
    book_data=BookDB()
    list_by_genre=[]
    genres = ["Fiction","Non-Fiction","Science","History","Other"]
    for genre in genres:
        count = book_data.count_by_genre(genre)
        if count>0:
            list_by_genre.append({"Genre":genre,"COUNT":count})
    book_data.close_db()
    return list_by_genre
    
@report_router.get("/top-member")
def top_member():
    member_data=MemberDB()
    top=member_data.get_top_member()
    return top
