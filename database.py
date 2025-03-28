import pymysql
from config import logger, Config
from datetime import datetime
from typing import List, Dict, Optional

class PaymentDatabase:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Connect to MySQL database."""
        try:
            self.connection = pymysql.connect(
                charset="utf8mb4",
                connect_timeout=Config.DB_TIMEOUT,
                cursorclass=pymysql.cursors.DictCursor,
                db=Config.DB_NAME,
                host=Config.DB_HOST,
                password=Config.DB_PASSWORD,
                read_timeout=Config.DB_TIMEOUT,
                port=Config.DB_PORT,
                user=Config.DB_USER,
                write_timeout=Config.DB_TIMEOUT,
            )
            print("Successfully connected to database")
        except Exception as e:
            print(f"Database connection error: {str(e)}")
            self.connection = None

    def ensure_connection(self):
        """Ensure database connection is active."""
        try:
            if self.connection is None or not self.connection.is_connected():
                logger.info("Reconnecting to database...")
                self.connect()
        except:
            self.connect()
        return self.connection is not None

    def get_user_history(self, userid: str) -> List[Dict]:
        """Get payment history for a specific user."""
        if not self.ensure_connection():
            logger.error("Failed to connect to database")
            return []
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, userid, amount
                FROM users 
                WHERE userid = %s 
                ORDER BY id DESC
            """
            cursor.execute(query, (userid,))
            results = cursor.fetchall()
            logger.info(f"Found {len(results)} transactions for user {userid}")
            cursor.close()
            return results
        except Exception as e:
            logger.error(f"Error retrieving user history: {str(e)}")
            return []

    def get_all_users(self) -> List[Dict]:
        """Get all users and their payments."""
        if not self.ensure_connection():
            logger.error("Failed to connect to database")
            return []
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, userid, amount,
                       COALESCE(transaction_date, NOW()) as transaction_date,
                       COALESCE(status, 'completed') as status
                FROM users 
                ORDER BY id DESC 
                LIMIT 5
            """
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            
            for result in results:
                if 'transaction_date' in result and result['transaction_date']:
                    result['transaction_date'] = result['transaction_date'].strftime('%Y-%m-%d %H:%M:%S')
            
            return results
        except Exception as e:
            logger.error(f"Error retrieving users: {str(e)}")
            return []
        
    def store_payment(self, userid: str, amount: float) -> bool:
        """Store payment details after QR generation."""
        if not self.ensure_connection():
            logger.error("Failed to connect to database")
            return False
            
        try:
            cursor = self.connection.cursor()
            query = """
                INSERT INTO users (userid, amount)
                VALUES (%s, %s)
            """
            cursor.execute(query, (userid, str(amount)))
            self.connection.commit()
            cursor.close()
            logger.info(f"Stored payment for user {userid} with amount ${amount}")
            return True
        except Exception as e:
            logger.error(f"Error storing payment: {str(e)}")
            return False

    def get_latest_payment(self) -> Optional[Dict]:
        """Get the most recent payment (admin only)."""
        if not self.ensure_connection():
            logger.error("Failed to connect to database")
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, userid, amount
                FROM users 
                ORDER BY id DESC 
                LIMIT 1
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            logger.error(f"Error retrieving latest payment: {str(e)}")
            return None
    
    def get_user_latest_payment(self, userid: str) -> Optional[Dict]:
        """Get the most recent payment for a specific user."""
        if not self.ensure_connection():
            logger.error("Failed to connect to database")
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            # Fixed SQL injection vulnerability by removing the stray "SELECT * FROM users;"
            query = """
                SELECT id, userid, amount
                FROM users 
                WHERE userid = %s
                ORDER BY id DESC 
                LIMIT 1
            """
            cursor.execute(query, (userid,))
            result = cursor.fetchone()
            cursor.close()
            logger.info(f"Retrieved latest payment for user {userid}")
            return result
        except Exception as e:
            logger.error(f"Error retrieving user's latest payment: {str(e)}")
            return None
    

# try:
#     cursor = connection.cursor()
#     ## YOUR SQL request code here
#     # cursor.execute("CREATE TABLE mytest (id INTEGER PRIMARY KEY)")
#     # cursor.execute("INSERT INTO mytest (id) VALUES (1), (2)")
#     # cursor.execute("SELECT * FROM mytest")
#     print(cursor.fetchall())
# finally:
#     connection.close()