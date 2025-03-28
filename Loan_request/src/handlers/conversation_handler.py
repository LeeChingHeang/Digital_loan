import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import re
import hashlib

from src.config.config import *
from src.utils.language_manager import LanguageManager
from src.database.db_manager import DatabaseManager
from src.utils.file_handler import FileHandler
from src.services.loan_processor import LoanProcessor
from src.services.reminder_service import ReminderService

logger = logging.getLogger(__name__)

class ConversationHandlerManager:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.file_handler = FileHandler()
        self.loan_processor = LoanProcessor()
        self.reminder_service = ReminderService()
        self.lang_manager = LanguageManager()

    async def start(self, update: Update, context: CallbackContext) -> int:
        """Start the conversation and ask for language preference"""
        context.user_data.clear()
        keyboard = [
            [InlineKeyboardButton("English", callback_data='english'),
             InlineKeyboardButton("ខ្មែរ", callback_data='khmer')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🌐 Welcome! Please choose your language:", 
                                      reply_markup=reply_markup)
        return SELECT_LANGUAGE

    async def language_selection(self, update: Update, context: CallbackContext) -> int:
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        language = query.data
        context.user_data['language'] = language
        context.user_data['telegram_id'] = query.from_user.id
        context.user_data['user_full_name'] = query.from_user.full_name

        keyboard = [
            [InlineKeyboardButton(self.lang_manager.get_message(language, 'new_user'), 
                                callback_data='new')],
            [InlineKeyboardButton(self.lang_manager.get_message(language, 'existing_user'), 
                                callback_data='existing')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            self.lang_manager.get_message(language, 'user_status_prompt'),
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return NEW_USER_CHOICE

    async def cancel(self, update: Update, context: CallbackContext) -> int:
        """Cancel the conversation"""
        self.file_handler.delete_temp_files(context)
        context.user_data.clear()
        language = context.user_data.get('language', 'english')
        cancel_text = self.lang_manager.get_message(language, 'loan_cancelled')
        
        if update.callback_query:
            await update.callback_query.message.reply_text(cancel_text, parse_mode="Markdown")
        else:
            await update.effective_message.reply_text(cancel_text, parse_mode="Markdown")
        
        return ConversationHandler.END

    async def auth_handler(self, update: Update, context: CallbackContext) -> int:
        """Handle user authentication"""
        language = context.user_data.get('language', 'english')
        telegram_id = update.effective_user.id
        user_input = update.message.text.strip()

        if user_input.isdigit() and len(user_input) == 6:
            # PIN authentication
            hashed_input = hashlib.sha256(user_input.encode('utf-8')).hexdigest()
            if self.db_manager.verify_pin(telegram_id, hashed_input):
                await update.message.reply_text(
                    self.lang_manager.get_message(language, 'auth_success'),
                    parse_mode="Markdown"
                )
                await self.proceed_to_loan_application(update, context)
                return SELECT_TENOR
            else:
                await update.message.reply_text(
                    self.lang_manager.get_message(language, 'incorrect_pin'),
                    parse_mode="Markdown"
                )
                return AUTHENTICATE
        elif user_input == str(telegram_id):
            # Telegram ID authentication
            await update.message.reply_text(
                self.lang_manager.get_message(language, 'auth_success_by_id'),
                parse_mode="Markdown"
            )
            await self.proceed_to_loan_application(update, context)
            return SELECT_TENOR
        else:
            await update.message.reply_text(
                self.lang_manager.get_message(language, 'incorrect_auth'),
                parse_mode="Markdown"
            )
            return AUTHENTICATE

    async def proceed_to_loan_application(self, update: Update, context: CallbackContext) -> None:
        """Proceed with loan application after successful authentication"""
        language = context.user_data.get('language', 'english')
        await update.message.reply_text(
            self.lang_manager.get_message(language, 'welcome'),
            parse_mode="Markdown"
        )
        
        tenor_keyboard = [
            [InlineKeyboardButton(option, callback_data=f"{i}w" if i < 4 else f"{i//4}m")
             for i, option in enumerate(self.lang_manager.get_message(language, 'tenor_options'), 2)],
            [InlineKeyboardButton("🚫 " + self.lang_manager.get_message(language, 'cancel'),
                                callback_data='cancel')]
        ]
        reply_markup = InlineKeyboardMarkup(tenor_keyboard)
        await update.message.reply_text(
            self.lang_manager.get_message(language, 'select_tenor'),
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # Additional handler methods would be implemented here...
    # For brevity, I've included the core handlers. The complete implementation
    # would include all conversation states defined in config.py

    def get_conversation_handler(self):
        """Return the configured ConversationHandler"""
        return ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                SELECT_LANGUAGE: [
                    CallbackQueryHandler(self.language_selection, pattern='^(english|khmer)$')
                ],
                # Additional states would be defined here...
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )