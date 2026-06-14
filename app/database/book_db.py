from database.db_connection import ConnectionMySql
import mysql.connector
import logging
logger= logging.getLogger(__name__)

class BookDB(ConnectionMySql):
        
    def create_book(self,data):
        key=", ".join(data.keys())
        places_holder= ", ".join(["%s"]*len(data))
        value=list(data.values())
        
        sql=f"INSERT INTO books({key}) VALUES ({places_holder})"
        self.cursor.execute(sql,value)
        logger.info("creating new book in sql")
        self.conn.commit()
        return self.cursor.lastrowid >0
        
    
    def get_all_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

        
    
    def get_book_by_id(self,id):
        self.cursor.execute("SELECT * FROM books WHERE id = %s",(id,))
        return self.cursor.fetchone()
        
    
    def update_book(self,id,data):
        key_data=", ".join([f"{key} = %s" for key in data.keys()])
        value=list(data.values())+[id]
        sql=f"UPDATE books SET {key_data} WHERE id = %s"
        self.cursor.execute(sql,value)
        self.conn.commit()
        return self.cursor.rowcount>0
    
    def set_available(self,id,val,member_id):
        try:
            is_available = val.lower()=="return"
            self.cursor.execute("SELECT borrowed_by_member_id FROM books WHERE id = %s",(id,))
            result=self.cursor.fetchone()
            if not result:
                return False
            if result[0] is not None:
                result=int(result[0])
            
            if is_available:
                if result == member_id:
                    self.cursor.execute("UPDATE books SET is_available =%s,borrowed_by_member_id=NULL WHERE id=%s",(True,id))
                else:
                    return False
            else:
                if result is None:
                    self.cursor.execute("UPDATE books SET is_available=%s,borrowed_by_member_id=%s WHERE id =%s",(False,member_id,id))
                else:
                    return False
            self.conn.commit()
                
        except:return False
        return True
            
    def count_total_books(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books")
            return self.cursor.fetchone()[0]
        except mysql.connector.Error:
            return 0
    
    def count_available_books(self):
        try: 
            self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = %s",(True,))
            return self.cursor.fetchone()[0]
        except:
            return 0
    
    def count_borrowed_books(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books WHERE is_available = %s",(False,))
            return self.cursor.fetchone()[0]
        except:
            return 0
    
    def count_by_genre(self,genre):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books WHERE genre = %s",(genre,))
            return self.cursor.fetchone()[0]
        except:
            return 0
    
    def count_active_borrows_by_member(self,member_id):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM books WHERE borrowed_by_member_id = %s",(member_id,))
            return self.cursor.fetchone()[0]
        except:
            return 0
    