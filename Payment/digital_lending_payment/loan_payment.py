from telegram.ext import CommandHandler
from config import logger
from database import PaymentDatabase
from Payment.digital_lending_payment.bot import PaymentBot

class PaymentService:
    """Service class to handle all payment-related functionality"""
    
    def __init__(self):
        """Initialize the payment service"""
        self.bot = PaymentBot()
        self.initialized = False
        
    def initialize(self):
        """Initialize database schema if needed"""
        try:
            db = PaymentDatabase()
            if db.ensure_connection():
                cursor = db.connection.cursor()
                
                # Check if users table exists, if not create it
                cursor.execute("SHOW TABLES LIKE 'users'")
                if not cursor.fetchone():
                    logger.info("Creating users table...")
                    cursor.execute("""
                        CREATE TABLE users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            userid VARCHAR(20) NOT NULL,
                            amount DECIMAL(10, 2) NOT NULL,
                            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            status ENUM('pending', 'completed', 'failed') DEFAULT 'completed',
                            payment_method VARCHAR(50) DEFAULT 'QR code',
                            notes TEXT
                        )
                    """)
                    cursor.execute("CREATE INDEX idx_userid ON users(userid)")
                    db.connection.commit()
                    logger.info("Users table created successfully")
                cursor.close()
            self.initialized = True
            return True
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            return False
    
    def register_handlers(self, application):
        """Register all payment-related handlers to the application"""
        if not self.initialized and not self.initialize():
            logger.error("Failed to initialize payment system")
            return False
        
        # Add all handlers to the main application
        application.add_handler(CommandHandler("pay", self.bot.start_command))
        application.add_handler(CommandHandler("payhelp", self.bot.help_command))
        application.add_handler(CommandHandler("status", self.bot.status_command))
        application.add_handler(CommandHandler("qr", self.bot.create_qr_command))
        application.add_handler(CommandHandler("history", self.bot.history_command))
        application.add_handler(CommandHandler("recent", self.bot.recent_command))
        
        # Add error handler
        application.add_error_handler(self.bot.error_handler)
        
        logger.info("Payment handlers registered successfully")
        return True
        
    async def process_payment_request(self, update, context):
        """Process a payment request from the button click"""
        return await self.bot.start_command(update, context)

# Create a singleton instance for import
payment_service = PaymentService()

# These functions are kept for backward compatibility and simplicity
def handle_loan_payment(application):
    return payment_service.register_handlers(application)

async def process_payment(update, context):
    return await payment_service.process_payment_request(update, context)