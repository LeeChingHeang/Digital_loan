import logging
from telegram.ext import ApplicationBuilder
from src.config.config import TOKEN
from src.database.db_manager import DatabaseManager
from src.handlers.conversation_handler import ConversationHandlerManager

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

    def run(self):
        """Start the bot"""
        try:
            # Create the Application and add handlers
            application = ApplicationBuilder().token(TOKEN).build()
            
            # Add the main conversation handler
            application.add_handler(self.conversation_manager.get_conversation_handler())
            
            # Start polling
            logger.info("Bot is starting...")
            application.run_polling()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

def main():
    """Main entry point for the application"""
    try:
        # Create and start the bot
        bot = LoanServiceBot()
        bot.setup()
        bot.run()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        raise

if __name__ == "__main__":
    main()