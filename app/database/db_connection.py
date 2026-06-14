import mysql.connector


def get_connection():
    return mysql.connector.Connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="library_db"
        )
    

class ConnectionMySql:
    def __init__(self):
        self.conn= get_connection()
        self.cursor=self.conn.cursor()
        
    def close_db(self):
        self.cursor.close()
        self.conn.close()
    

def create_tables():
    conn = get_connection()
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS books(
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(50) NOT NULL,
        author VARCHAR(50) NOT NULL,
        genre ENUM("Fiction","Non-Fiction","Science","History","Other") NOT NULL,
        is_available BOOLEAN DEFAULT TRUE,
        borrowed_by_member_id INT DEFAULT NULL
    )   
    """)
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS members(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        is_active BOOLEAN DEFAULT True,
        total_borrows INT NOT NULL
    )   
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
    
    
    