from fastapi import FastAPI
import uvicorn
from routes.book_routes import book_router
from routes.member_routes import member_router
from routes.report_routes import report_router
from database.db_connection import create_tables
import logging

app=FastAPI()
logging.basicConfig(level=logging.DEBUG,format= "%(asctime)s | %(levelname)s | %(message)s",
                    handlers=[logging.FileHandler("app/logs/app.log"),logging.StreamHandler()])
app.include_router(book_router,prefix="/books")
app.include_router(member_router,prefix="/members")
app.include_router(report_router,prefix="/reports")



if __name__=="__main__":
    create_tables()
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)
    
