import logging
from telegram.ext import ApplicationBuilder
from Loan_request.src.config.config import TOKEN
from Loan_request.src.database.db_manager import DatabaseManager
from Loan_request.src.handlers.conversation_handler import ConversationHandlerManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class LoanServiceBot:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conversation_manager = ConversationHandlerManager()

    def setup(self):
        """Initialize the bot and set up necessary components"""
        # Initialize database tables
        self.db_manager.create_tables()
        logger.info("Database tables initialized")

    def get_conversation_handler(self):
        """Get the conversation handler for loan requests"""
        return self.conversation_manager.get_conversation_handler()
