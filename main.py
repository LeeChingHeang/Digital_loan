from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from config import Config, logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater

# Import functions from separate scripts
from Payment.digital_lending_payment.loan_payment import payment_service, process_payment
from Loan_request.Loan_service import loan_service

# Import the general info service
from General_Information.general_loan import general_info_service

def get_general_info():
    return "General information"
load_dotenv()  # Load variables from .env file

# Define the command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Button Keyboard Reply
    general_info_button = KeyboardButton(text="General Info")
    request_loan_button = KeyboardButton(text="Request Loan")
    pay_loan_button = KeyboardButton(text="Pay Loan")
    keyboard = ReplyKeyboardMarkup(
        [[general_info_button], [request_loan_button], [pay_loan_button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await update.message.reply_text('Hello! I am your bot. Use the buttons below for different options.', reply_markup=keyboard)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Start the general info flow instead of just sending text
    await general_info_service.start_info(update, context)

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Use the process_payment function for consistent behavior
    await process_payment(update, context)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    logger.info(f"Button click received with text: {text}")
    if text == "General Info":
        await info(update, context)
    elif text == "Pay Loan":
        await pay(update, context)

def main() -> None:
    """Start the bot."""
    TOKEN = Config.TELEGRAM_BOT_TOKEN
    BASE_URL = Config.BASE_URL
    
    application = Application.builder().token(TOKEN).build()
    # application = Application.builder().token(TOKEN).base_url(BASE_URL).build()

    # Initialize loan service first
    loan_service.setup()
    
    # Debug handler to log all messages
    async def debug_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.message:
            if update.message.text:
                logger.info(f"Message received: {update.message.text}")
            else:
                logger.info(f"Non-text message received: {update.message}")
        return None

    # Register handlers in order of priority
    # Group -1: Debug logging (runs before all handlers)
    application.add_handler(MessageHandler(filters.ALL, debug_handler), group=-1)
    
    # Group 0: Core handlers
    application.add_handler(CommandHandler("start", start), group=0)
    loan_service.register_handlers(application)  # Also in group 0
    
    # Group 1: Service handlers
    payment_service.register_handlers(application)
    general_info_service.register_handlers(application)
    
    # Group 2: Fallback handlers
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.Regex("^Request Loan$"), 
        button_click
    ), group=2)
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()
