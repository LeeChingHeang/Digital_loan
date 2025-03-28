import logging
import hashlib
import pymysql
import re
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """Establish database connection"""
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
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def ensure_connection(self):
        """Ensure database connection is active"""
        try:
            self.connection.ping(reconnect=True)
        except:
            self.connect()

    def create_tables(self):
        """Create necessary database tables"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        telegram_id BIGINT UNIQUE,
                        user_unique_id VARCHAR(36),
                        national_id VARCHAR(255),
                        user_pin_hash VARCHAR(255),
                        national_id_hash VARCHAR(255),
                        tenor VARCHAR(50),
                        amount INT,
                        document_path VARCHAR(255),
                        id_card_path VARCHAR(255),
                        extracted_id_data TEXT,
                        selfie_path VARCHAR(255),
                        work_duration INT,
                        factory_workers INT,
                        factory_locations INT,
                        factory_origin VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)

                # Questions table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS questions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        question_text TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)

                # Feedback table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        telegram_id BIGINT,
                        feedback_text TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)

                self.connection.commit()
                logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise

    def store_user_data(self, telegram_id, tenor, amount, doc_path, id_path, extracted_data, 
                       selfie_path, work_duration, factory_workers, factory_locations, 
                       factory_origin, national_id: str = None):
        """Store or update user data"""
        self.ensure_connection()
        try:
            # Data validation and cleaning
            amount = int(float(str(amount).strip())) if amount else 0
            work_duration = int(float(str(work_duration).strip())) if work_duration else 0
            factory_workers = int(float(str(factory_workers).strip())) if factory_workers else 0
            factory_locations = int(float(str(factory_locations).strip())) if factory_locations else 0

            if national_id:
                national_id = re.sub(r'[\s\-\n]', '', national_id)
                national_id_hash = hashlib.sha256(national_id.encode('utf-8')).hexdigest()
            else:
                national_id_hash = None

            with self.connection.cursor() as cursor:
                # Check if user exists
                cursor.execute("SELECT id FROM users WHERE telegram_id = %s", (telegram_id,))
                user_exists = cursor.fetchone()

                if user_exists:
                    # Update existing user
                    cursor.execute("""
                        UPDATE users SET
                            tenor = %s,
                            amount = %s,
                            document_path = %s,
                            id_card_path = %s,
                            extracted_id_data = %s,
                            selfie_path = %s,
                            work_duration = %s,
                            factory_workers = %s,
                            factory_locations = %s,
                            factory_origin = %s,
                            national_id = COALESCE(%s, national_id),
                            national_id_hash = COALESCE(%s, national_id_hash)
                        WHERE telegram_id = %s
                    """, (tenor, amount, doc_path, id_path, extracted_data, selfie_path,
                          work_duration, factory_workers, factory_locations, factory_origin,
                          national_id, national_id_hash, telegram_id))
                else:
                    # Insert new user
                    cursor.execute("""
                        INSERT INTO users (
                            telegram_id, tenor, amount, document_path, id_card_path,
                            extracted_id_data, selfie_path, work_duration, factory_workers,
                            factory_locations, factory_origin, national_id, national_id_hash
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (telegram_id, tenor, amount, doc_path, id_path, extracted_data,
                          selfie_path, work_duration, factory_workers, factory_locations,
                          factory_origin, national_id, national_id_hash))

                self.connection.commit()
                logger.info(f"User data saved for Telegram ID {telegram_id}")
        except Exception as e:
            logger.error(f"Error storing user data: {e}")
            self.connection.rollback()
            raise

    def load_user_data(self, telegram_id: int) -> dict:
        """Load user data from database"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    SELECT document_path, id_card_path, extracted_id_data, selfie_path,
                           national_id, tenor, amount, work_duration, factory_workers,
                           factory_locations, factory_origin
                    FROM users 
                    WHERE telegram_id = %s
                """, (telegram_id,))
                result = cursor.fetchone()
                return result if result else {}
        except Exception as e:
            logger.error(f"Error loading user data: {e}")
            return {}

    def user_has_pin(self, telegram_id: int) -> bool:
        """Check if user has set a PIN"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT user_pin_hash FROM users WHERE telegram_id = %s", (telegram_id,))
                result = cursor.fetchone()
                return bool(result and result['user_pin_hash'])
        except Exception as e:
            logger.error(f"Error checking user PIN: {e}")
            return False

    def verify_pin(self, telegram_id: int, pin_hash: str) -> bool:
        """Verify user's PIN"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT user_pin_hash FROM users WHERE telegram_id = %s", (telegram_id,))
                result = cursor.fetchone()
                return bool(result and result['user_pin_hash'] == pin_hash)
        except Exception as e:
            logger.error(f"Error verifying PIN: {e}")
            return False

    def store_question(self, question_text: str) -> None:
        """Store a question in the database"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("INSERT INTO questions (question_text) VALUES (%s)", (question_text,))
                self.connection.commit()
                logger.info(f"Question stored: {question_text}")
        except Exception as e:
            logger.error(f"Error storing question: {e}")
            self.connection.rollback()

    def store_feedback(self, telegram_id: int, feedback_text: str) -> None:
        """Store user feedback"""
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO feedback (telegram_id, feedback_text) VALUES (%s, %s)",
                    (telegram_id, feedback_text)
                )
                self.connection.commit()
                logger.info(f"Feedback stored for Telegram ID {telegram_id}")
        except Exception as e:
            logger.error(f"Error storing feedback: {e}")
            self.connection.rollback()

    def __del__(self):
        """Close database connection on object destruction"""
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
