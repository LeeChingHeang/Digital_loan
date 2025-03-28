from dotenv import load_dotenv
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from config import Config, logger
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, Updater

# Import functions from separate scripts
from Payment.digital_lending_payment.loan_payment import payment_service, process_payment
# from Loan_request.loan_request import loan_service, process_loan_request

# Import the general info service
from General_Information.general_loan import general_info_service

def get_general_info():
    return "General information"
def process_loan_request():
    return "Loan request"
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

async def loan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Use the process_loan_request function from the loan module
    # await process_loan_request(update, context)
    response = process_loan_request()
    await update.message.reply_text(response)

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Use the process_payment function for consistent behavior
    await process_payment(update, context)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "General Info":
        await info(update, context)
    elif text == "Request Loan":
        await loan(update, context)
    elif text == "Pay Loan":
        await pay(update, context)

def main() -> None:
    """Start the bot."""
    TOKEN = Config.TELEGRAM_BOT_TOKEN
    BASE_URL = Config.BASE_URL
    
    application = Application.builder().token(TOKEN).build()
    # application = Application.builder().token(TOKEN).base_url(BASE_URL).build()

    # Add standard command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Register all payment handlers
    payment_service.register_handlers(application)
    
    # Register all general info handlers
    general_info_service.register_handlers(application)
    
    # Register all loan request handlers
    # loan_service.register_handlers(application)
    
    # Add message handler for button clicks
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_click))
    
    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    main()