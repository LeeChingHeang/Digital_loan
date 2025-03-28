import asyncio
import os
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from cryptography.fernet import Fernet  # For encryption

# # Set up logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# # Load bot token
# TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8116272316:AAHI5jabceaEiqCsIMAmFwp-Kv-Fj6g21kE")

# Define categories, questions, and answers
CATEGORIES = {
    "kh": {
        "category1": "អំពីស្ថាប័ណ្ណ",
        "category2": "លក្ខខណ្ឌរបស់អតិថិជន",
        "category3": "ពាក្យសុំឥណទាន",
        "category4": "ការសង់ប្រាក់កម្ចី"
    },
    "en": {
        "category1": "About Us",
        "category2": "Term and Condition",
        "category3": "How to Request",
        "category4": "Pay Back"
    }
}

QUESTIONS = {
    "kh": {
        "category1": {
            1: "តើស្ថាប័ណ្ណខាងបងជាក្រុមហ៊ុន ឬក៏ជាមីក្រូ ឬក៏ជាធនាគារ?",
            2: "តើកម្ចី 8Stars Finance Digital Loan គឺជាអ្វី?",
            3: "ហេតុអ្វីបានជាខ្ញុំត្រូវជ្រើសរើសប្រើប្រាស់កម្ចី 8Stars Finance ឌីជីថលឡូន?",
            4: "តើខ្ញុំអាចដឹងថាសំណើកម្ចីរបស់ខ្ញុំត្រូវបានអនុម័តដោយរបៀបណា?",
            5: "បើខ្ញុំមានសំណួរផ្សេងទៀតអំពីប្រាក់កម្ចីឌីជីថល 8Stars Finance តើខ្ញុំគួរទំនាក់ទំនងទៅអ្នកណា?"
        },
        "category2": {
            6: "តើតម្រូវឲ្យមានឯកសារអ្វីខ្លះដើម្បីស្នើសុំកម្ចី?",
            7: "តើ អ្នកណាដែលមានសិទ្ធដាក់ពាក្យសុំប្រាក់កម្ចីឌីជីថល 8Stars Finance?"
        },
        "category3": {
            8: "ខ្ញុំមិនចេះស្នើកម្ចីដោយខ្លួនឯងទេ តើអ្នកណាអាចជួយស្នើឲ្យខ្ញុំបានដែរឬទេ?",
            9: "តើខ្ញុំអាចស្នើកម្ចី 8Stars Finance ឌីជីថលឡូនបានដោយរបៀបណា?",
            10: "តើខ្ញុំអាចស្នើកម្ចីជាលើកទី 2 បានដែរឬទេ?"
        },
        "category4": {
            11: "តើខ្ញុំអាចបង់សងប្រចាំខែតាមរបៀបណាខ្លះ?",
            12: "តើខ្ញុំអាចបង់ផ្ដាច់កម្ចីនេះតាមរបៀបណា?"
        }
    },
    "en": {
        "category1": {
            1: "Is your institution a company, a microfinance institution, or a bank?",
            2: "What is 8Stars Finance Digital Loan?",
            3: "Why should I choose to apply for an 8Stars Finance Digital Loan?",
            4: "How will I know if I'm Approved? How can I check my loan application status?",
            5: "If I have more questions about 8Stars Finance Digital Loan, who should I contact?",
        },
        "category2": {
            6: "What documents are required to apply for the loan?",
            7: "Who is eligible to apply for the 8Stars Finance Digital Loan?"
        },
        "category3": {
            8: "I don't know how to apply, can I ask someone to apply for me?",
            9: "How can I apply for an 8Stars Finance Digital Loan?",
            10: "Is it possible to have more than one loan at a time?"
        },
        "category4": {
            11: "How can I pay for the monthly installment?",
            12: "How can I pay off the loan?"
        }
    }
}

ANSWERS = {
    "kh": {
        1: "យើងជាគ្រឹះស្ថានមានអាជ្ញារប័ណ្ណក្រោមធនាគារជាតិនៃកម្ពុជា។",
        2: "កម្ចី 8Stars Finance Digital Loan គឺជាកម្ចីឌីជីថិល",
        3: "ព្រោះកម្ចី 8Stars Finance ឌីជីថលឡូនមានភាពងាយស្រួល រហ័ស និងអាចទទួលបានការអនុមតភ្លាមៗ ដោយមិនចាំបាច់រង់ចាំយូរ។",
        4: "អ្នកនឹងទទួលបានសារជូនដំណឹងតាមរយៈកាហៅទូរស័ព្ទពីបុគ្គលិក ឬសារ (SMS) នៅពេលដែលកម្ចីត្រូវបានអនុមត។",
        5: "អ្នកអាចទំនាក់ទំនងទៅសេវាកម្មអតិថិជន 8Stars Finance តាមរយៈ៖ 023 934444 និងប្រព័ន្ធ ផ្សព្វផ្សាយ សង្គមរបស់យើង។",
        6: "តម្រូវអោយមាន ឯកសារចម្បងមួយចំនួន ដូចជារូបថតអត្តសញ្ញាណប័ណ្ណនិងលិខិតបញ្ជាក់ប្រាក់ចំណូលរបស់អ្នក។",
        7: "អតិថិជនទាំងអស់ដែលមានអាយុចាប់ពី 18 - 65 ឆ្នាំ។",
        8: "ប្រាកដណាស់ អ្នកអាចទាក់ទងទៅលេខ 023934444 ឬមើលតាមរយះ វីឌីអូដើម្បីស្នើកម្ចីបាន។",
        9: "អ្នកអាចស្នើកម្ចី 8Stars Finance ឌីជីថលឡូននេះបាន តាម 8Stars Finance Bots/ App, ។ សម្រាប់ព័ត៌មានលម្អិតពីរបៀបស្នើសុំ សូមចុច Link..",
        10: "អ្នកអាចមានកម្ចីតែមួយក្នុងពេលតែមួយ។",
        11: "អ្នកអាចបង់សងត្រឡប់តាមរយះ KHQR or Wing, TrueMoney",
        12: "អ្នកអាចបង់ផ្ដាច់កម្ចីឌីជីថលឡូននេះបានតាមអេប KHQR& 8Stars Finance, Wing, True Money."
    },
    "en": {
        1: "We are a Microfinance institution licensed under the National Bank of Cambodia.",
        2: "8Stars Finance Digital Loan is an online loan service.",
        3: "Because 8Stars Finance Digital Loan are easy, fast, and can be approved and disbursed instantly. No waiting time.",
        4: "You will receive a phone call from staff, notification, or SMS when your loan is approved. You can also check your application or loan status by tapping 8Stars Finance Digital Loan function in 8Stars Finance Bots/App.",
        5: "You can contact 8Stars Finance Customer Service via 023 934444 and our social media platforms.",
        6: "Required documents include a photo of your ID card and proof of income.",
        7: "All customers between the ages of 18 and 65 are eligible.",
        8: "Yes, you can call 023934444 or check the video via link to apply for the loan.",
        9: "You can apply for a Digital Loan via 8Stars Finance Bots/App. For more details on how to apply, please click here.",
        10: "You are only eligible for one loan at a time.",
        11: "You can pay for the monthly installment via KHQR or Wing, TrueMoney.",
        12: "You can pay off the loan via KHQR & 8Stars Finance, Wing, TrueMoney."
    }
}

# Encryption setup
KEY_FILE = "encryption_key.key"

def load_or_generate_key():  
    """Load the encryption key from a file or generate a new one if it doesn't exist."""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

# Initialize the Fernet cipher with the key
encryption_key = load_or_generate_key()
cipher = Fernet(encryption_key)

# ----------------------------------------------
# Helper Functions
# ----------------------------------------------

def create_keyboard(options, prefix=""):
    """Generate an inline keyboard from a dictionary of options."""
    return [[InlineKeyboardButton(text, callback_data=f"{prefix}{key}")] for key, text in options.items()]

# ----------------------------------------------
# Bot Handlers
# ----------------------------------------------

# Create a service class to organize the functionality
class GeneralInfoService:
    def __init__(self):
        self.cipher = Fernet(load_or_generate_key())

    async def start_info(selft, update: Update, context):
        """Start command: Ask user to select language."""
        try:
            keyboard = create_keyboard({"kh": "ភាសាខ្មែរ", "en": "English"}, "lang_")
            await update.message.reply_text(
                "សួស្តី! សូមជ្រើសរើសភាសារបស់អ្នក។ Hello! Please choose your language ❤️:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await update.message.reply_text("Sorry, something went wrong. Please try again later.")
            logging.error(f"Error in start: {e}")

    async def language_selection(self, update: Update, context):
        """Handle language selection and show categories."""
        try:
            query = update.callback_query
            lang = query.data.split("_")[1]
            context.user_data["language"] = lang
            context.user_data["history"] = []
            context.user_data["category"] = None
            await self.display_categories(query, context, lang)
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in language_selection: {e}")

    async def display_categories(self, query, context, lang):
        """Display categories to the user."""
        try:
            keyboard = create_keyboard(CATEGORIES[lang], "cat_")
            await query.edit_message_text(
                "សូមជ្រើសរើសប្រភេទ:" if lang == "kh" else "Choose a category:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in display_categories: {e}")

    async def category_selection(self, update: Update, context):
        """Handle category selection and display questions."""
        try:
            query = update.callback_query
            lang = context.user_data.get("language", "en")
            category_key = query.data.split("_")[1]
            context.user_data["category"] = category_key
            await self.display_questions(query, context, lang, category_key)
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in category_selection: {e}")

    async def display_questions(self, query, context, lang, category_key):
        """Display questions for the selected category, excluding answered ones."""
        try:
            questions = QUESTIONS[lang].get(category_key, {})
            answered_questions = set(context.user_data.get("history", []))
            remaining_questions = {q_id: q for q_id, q in questions.items() if q_id not in answered_questions}

            keyboard = create_keyboard(remaining_questions, "q_")
            if not remaining_questions:
                end_text = "បញ្ចប់" if lang == "kh" else "End"
                keyboard.append([InlineKeyboardButton(end_text, callback_data="end")])

            await query.edit_message_text(
                "សូមជ្រើសរើសសំណួរ:" if lang == "kh" else "Choose a question:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in display_questions: {e}")

    async def button_handler(self, update: Update, context):
        """Handle question selection, store encrypted question in a file, and show answers."""
        try:
            query = update.callback_query
            lang = context.user_data.get("language", "en")
            question_id = int(query.data.split("_")[1])

            # Store the question ID in history
            context.user_data.setdefault("history", []).append(question_id)

            # Get the full question text for logging
            category_key = context.user_data.get("category")
            question_text = QUESTIONS[lang].get(category_key, {}).get(question_id, "Question not found")

            # Create the log entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Language: {lang} - Question: {question_text}\n"

            # Encrypt the log entry
            encrypted_entry = self.cipher.encrypt(log_entry.encode("utf-8"))

            # Write the encrypted entry to the file
            with open("user_questions1.txt", "ab") as f:  # 'ab' for append in binary mode
                f.write(encrypted_entry + b"\n")  # Add newline for separation

            # Build the response text showing full history
            response_text = ""
            for q_id in context.user_data["history"]:
                response_text += f"**Q:** {QUESTIONS[lang].get(context.user_data['category'], {}).get(q_id, '')}\n**A:** {ANSWERS[lang].get(q_id, 'No answer available.')}\n\n"

            # Language-specific button texts
            back_text = "ត្រឡប់ក្រោយ" if lang == "kh" else "<< Go Back"
            end_text = "បញ្ចប់" if lang == "kh" else "End"
            
            keyboard = [
                [InlineKeyboardButton(back_text, callback_data="back")],
                [InlineKeyboardButton(end_text, callback_data="end")]
            ]

            await query.edit_message_text(
                response_text.strip(),
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in button_handler: {e}")

    async def back_to_menu(self, update: Update, context):
        """Return to the question menu for the current category."""
        try:
            query = update.callback_query
            lang = context.user_data.get("language", "en")
            category_key = context.user_data.get("category", None)

            if category_key:
                await self.display_questions(query, context, lang, category_key)
            else:
                await self.display_categories(query, context, lang)
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in back_to_menu: {e}")

    async def end_handler(self, update: Update, context):
        """End the conversation."""
        try:
            query = update.callback_query
            lang = context.user_data.get("language", "en")
            
            # Language-specific button text
            start_over_text = "ចាប់ផ្តើមឡើងវិញ" if lang == "kh" else "Start Over"

            await query.edit_message_text(
                "សូមអរគុណ! ការសន្ទនាបានបញ្ចប់។ ❤️" if lang == "kh" else "Thank you! The conversation has ended. ❤️",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(start_over_text, callback_data="start_over")]])
            )
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in end_handler: {e}")

    async def start_over(self, update: Update, context):
        """Return to language selection and reset the conversation."""
        try:
            query = update.callback_query
            context.user_data.clear()  # Reset all user data
            keyboard = create_keyboard({"kh": "ភាសាខ្មែរ", "en": "English"}, "lang_")

            await query.edit_message_text(
                "សួស្តី! សូមជ្រើសរើសភាសារបស់អ្នក ❤️:" if context.user_data.get("language", "en") == "kh" else "សួស្តី! សូមជ្រើសរើសភាសារបស់អ្នក។ Hello! Please choose your language ❤️:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            await query.answer()
        except Exception as e:
            await query.edit_message_text("Sorry, something went wrong. Please try again.")
            logging.error(f"Error in start_over: {e}")

    # ----------------------------------------------
    # Main Application
    # ----------------------------------------------

    def register_handlers(self, application):
        """Set up and run the bot."""
        try:

            application.add_handler(CommandHandler("info", self.start_info))
            application.add_handler(CallbackQueryHandler(self.language_selection, pattern="^lang_"))
            application.add_handler(CallbackQueryHandler(self.category_selection, pattern="^cat_"))
            application.add_handler(CallbackQueryHandler(self.button_handler, pattern="^q_"))
            application.add_handler(CallbackQueryHandler(self.back_to_menu, pattern="^back$"))
            application.add_handler(CallbackQueryHandler(self.end_handler, pattern="^end$"))
            application.add_handler(CallbackQueryHandler(self.start_over, pattern="^start_over$"))

            logging.info("General info handlers registered successfully")
        except Exception as e:
            logging.error(f"Failed to start bot: {e}")


# Create an instance of the service to be imported
general_info_service = GeneralInfoService()




