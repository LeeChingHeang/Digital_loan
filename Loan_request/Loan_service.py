import logging
from Loan_request.src.database.db_manager import DatabaseManager
from Loan_request.src.handlers.conversation_handler import ConversationHandlerManager

logger = logging.getLogger(__name__)

class LoanService:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.conversation_manager = ConversationHandlerManager()

    def setup(self):
        """Initialize the loan service components"""
        # Initialize database tables
        self.db_manager.create_tables()

    def register_handlers(self, application):
        """Register all handlers for the loan service"""
        logger.info("Registering loan service handlers")
        # Add the main conversation handler for loan requests with high priority
        handler = self.conversation_manager.get_conversation_handler()
        application.add_handler(handler, group=0)  # Group 0 has highest priority
        logger.info("Loan conversation handler registered with group 0")

# Create a singleton instance
loan_service = LoanService()
