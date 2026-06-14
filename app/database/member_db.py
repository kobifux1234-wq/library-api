from database.db_connection import ConnectionMySql
import logging
logger =logging.getLogger(__name__)
    
    
class MemberDB(ConnectionMySql):
    def create_member(self,data):
        key=", ".join(data.keys())
        placeholders = ", ".join(["%s"]*len(data))
        sql=f"INSERT INTO members({key}) VALUES ({placeholders})"
        self.cursor.execute(sql,list(data.values()))
        self.conn.commit()
        logger.info("new member is created")
        return self.cursor.lastrowid > 0
    
    def get_all_members(self):
        dict_cursor=self.conn.cursor(dictionary=True)
        try:
            dict_cursor.execute("SELECT * FROM members")
            return dict_cursor.fetchall()
        finally:dict_cursor.close()
    
    def get_member_by_id(self,id):
        self.cursor.execute("SELECT * FROM members WHERE id = %s",(id,))
        return self.cursor.fetchone()
    
    def update_member(self,id, data):
        sql_keys=", ".join([f"{key}= %s" for key in data.keys()])
        sql=f"UPDATE members SET {sql_keys} WHERE id = %s"
        val=list(data.values())+[id]
        self.cursor.execute(sql,val)
        self.conn.commit()
        logger.info("updated member")
        return self.cursor.rowcount>0
    
    def deactivate_member(self,id):
        self.cursor.execute("UPDATE members SET is_active= %s  WHERE id = %s",(False,id))
        self.conn.commit()
        logger.info(f"the member {id} is not-active")
        return self.cursor.rowcount>0
    
    def activate_member(self,id):
        self.cursor.execute("UPDATE members SET is_active= %s  WHERE id = %s",(True,id))
        self.conn.commit()
        logger.info(f"the member {id} is active")
        return self.cursor.rowcount>0
    
    
    def increment_borrows(self,id):
        self.cursor.execute("UPDATE members SET total_borrows = total_borrows+1 WHERE id=%s",(id,))
        self.conn.commit()
        return self.cursor.rowcount>0
        
    
    def count_active_members(self):
        self.cursor.execute("SELECT COUNT(*) FROM members WHERE is_active = True")
        return self.cursor.fetchone()[0]
    
    def get_top_member(self):
        self.cursor.execute("SELECT * FROM members ORDER BY total_borrows DESC LIMIT 1")
        return self.cursor.fetchone()
