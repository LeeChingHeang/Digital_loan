import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters
)

logger = logging.getLogger(__name__)

# Define conversation states
(SELECT_LANGUAGE, NEW_USER_CHOICE, AUTHENTICATE, SELECT_TENOR,
 SELECT_AMOUNT, UPLOAD_DOC, UPLOAD_ID, ID_CONFIRMATION,
 UPLOAD_SELFIE, USER_INFO) = range(10)

class ConversationHandlerManager:
    """Manage the conversation flow for loan requests"""

    def __init__(self):
        """Initialize the conversation handler manager"""
        logger.info("Initializing ConversationHandlerManager")

    async def start_conversation(self, update: Update, context: CallbackContext) -> int:
        """Start the conversation and ask for language preference"""
        logger.info(f"Starting loan request conversation. Message: {update.message.text if update.message else 'No message'}")
        context.user_data.clear()
        logger.info("User data cleared")
        
        try:
            logger.info("Setting up language selection keyboard")
            keyboard = [
                [InlineKeyboardButton("English", callback_data='english'),
                 InlineKeyboardButton("ខ្មែរ", callback_data='khmer')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            logger.info("Sending language selection message")
            await update.message.reply_text(
                "🌐 Welcome! Please choose your language:", 
                reply_markup=reply_markup
            )
            logger.info("Language selection message sent successfully")
        except Exception as e:
            logger.error(f"Error in start_conversation: {str(e)}")
            raise
        return SELECT_LANGUAGE

    async def language_selection(self, update: Update, context: CallbackContext) -> int:
        """Handle language selection"""
        try:
            logger.info("Processing language selection")
            query = update.callback_query
            await query.answer()
            
            selected_language = query.data
            logger.info(f"Selected language: {selected_language}")
            context.user_data['language'] = selected_language
            
            logger.info("Setting up user type selection keyboard")
            keyboard = [
                [InlineKeyboardButton("New User", callback_data='new'),
                 InlineKeyboardButton("Existing User", callback_data='existing')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            logger.info("Sending user type selection message")
            await query.message.reply_text(
                "Are you a new or existing user?",
                reply_markup=reply_markup
            )
            logger.info("User type selection message sent successfully")
            return NEW_USER_CHOICE
        except Exception as e:
            logger.error(f"Error in language_selection: {str(e)}")
            raise

    async def handle_user_choice(self, update: Update, context: CallbackContext) -> int:
        """Handle user type selection"""
        query = update.callback_query
        await query.answer()
        
        user_type = query.data
        context.user_data['user_type'] = user_type
        
        if user_type == 'existing':
            await query.message.reply_text(
                "Please enter your phone number for authentication:"
            )
            return AUTHENTICATE
        else:
            keyboard = [
                [InlineKeyboardButton("1 week", callback_data='1w'),
                 InlineKeyboardButton("2 weeks", callback_data='2w')],
                [InlineKeyboardButton("1 month", callback_data='1m'),
                 InlineKeyboardButton("2 months", callback_data='2m')],
                [InlineKeyboardButton("Cancel", callback_data='cancel')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Please select your preferred loan duration:",
                reply_markup=reply_markup
            )
            return SELECT_TENOR

    async def auth_handler(self, update: Update, context: CallbackContext) -> int:
        """Handle user authentication"""
        phone_number = update.message.text
        context.user_data['phone_number'] = phone_number
        
        keyboard = [
            [InlineKeyboardButton("1 week", callback_data='1w'),
             InlineKeyboardButton("2 weeks", callback_data='2w')],
            [InlineKeyboardButton("1 month", callback_data='1m'),
             InlineKeyboardButton("2 months", callback_data='2m')],
            [InlineKeyboardButton("Cancel", callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Please select your preferred loan duration:",
            reply_markup=reply_markup
        )
        return SELECT_TENOR

    async def handle_tenor_selection(self, update: Update, context: CallbackContext) -> int:
        """Handle loan tenor selection"""
        query = update.callback_query
        await query.answer()
        
        selected_tenor = query.data
        context.user_data['tenor'] = selected_tenor
        
        await query.message.reply_text(
            "Please enter your desired loan amount:"
        )
        return SELECT_AMOUNT

    async def handle_amount(self, update: Update, context: CallbackContext) -> int:
        """Handle loan amount input"""
        amount = update.message.text
        context.user_data['amount'] = amount
        
        await update.message.reply_text(
            "Please upload your salary slip or bank statement:"
        )
        return UPLOAD_DOC

    async def handle_doc_upload(self, update: Update, context: CallbackContext) -> int:
        """Handle document upload"""
        file_id = update.message.document.file_id if update.message.document else update.message.photo[-1].file_id
        context.user_data['doc_file_id'] = file_id
        
        await update.message.reply_text(
            "Please upload a photo of your ID card:"
        )
        return UPLOAD_ID

    async def handle_id_upload(self, update: Update, context: CallbackContext) -> int:
        """Handle ID card upload"""
        file_id = update.message.document.file_id if update.message.document else update.message.photo[-1].file_id
        context.user_data['id_file_id'] = file_id
        
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='yes'),
             InlineKeyboardButton("No", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Is your ID card clear and valid?",
            reply_markup=reply_markup
        )
        return ID_CONFIRMATION

    async def handle_id_confirmation(self, update: Update, context: CallbackContext) -> int:
        """Handle ID confirmation"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'yes':
            await query.message.reply_text(
                "Please take a selfie holding your ID card:"
            )
            return UPLOAD_SELFIE
        else:
            await query.message.reply_text(
                "Please upload a clearer photo of your ID card:"
            )
            return UPLOAD_ID

    async def handle_selfie_upload(self, update: Update, context: CallbackContext) -> int:
        """Handle selfie upload"""
        file_id = update.message.photo[-1].file_id
        context.user_data['selfie_file_id'] = file_id
        
        await update.message.reply_text(
            "Please enter your full name and address:"
        )
        return USER_INFO

    async def handle_user_info(self, update: Update, context: CallbackContext) -> int:
        """Handle user information input"""
        user_info = update.message.text
        context.user_data['user_info'] = user_info
        
        # Process the loan application
        await update.message.reply_text(
            "Thank you for your application. We will process it and get back to you soon."
        )
        return ConversationHandler.END

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        """Cancel the conversation"""
        if update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(
                "Loan application cancelled."
            )
        else:
            await update.message.reply_text(
                "Loan application cancelled."
            )
        return ConversationHandler.END

    def get_conversation_handler(self):
        """Return the configured ConversationHandler"""
        logger.info("Creating conversation handler")
        handler = ConversationHandler(
            entry_points=[
                MessageHandler(filters.Regex('^Request Loan$'), self.start_conversation)
            ],
            states={
                SELECT_LANGUAGE: [
                    CallbackQueryHandler(self.language_selection, pattern='^(english|khmer)$')
                ],
                NEW_USER_CHOICE: [
                    CallbackQueryHandler(self.handle_user_choice, pattern='^(new|existing)$')
                ],
                AUTHENTICATE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.auth_handler)
                ],
                SELECT_TENOR: [
                    CallbackQueryHandler(self.handle_tenor_selection, pattern='^[0-9]+[wm]$'),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                SELECT_AMOUNT: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_amount),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                UPLOAD_DOC: [
                    MessageHandler(filters.Document.ALL | filters.PHOTO, self.handle_doc_upload),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                UPLOAD_ID: [
                    MessageHandler(filters.Document.ALL | filters.PHOTO, self.handle_id_upload),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                ID_CONFIRMATION: [
                    CallbackQueryHandler(self.handle_id_confirmation),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                UPLOAD_SELFIE: [
                    MessageHandler(filters.PHOTO, self.handle_selfie_upload),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ],
                USER_INFO: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_user_info),
                    CallbackQueryHandler(self.cancel, pattern='^cancel$')
                ]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        logger.info("Conversation handler created successfully")
        return handler
