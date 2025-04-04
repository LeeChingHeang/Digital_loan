# bot.py
from datetime import datetime
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from config import Config, logger
from database import PaymentDatabase
from Payment.digital_lending_payment.qr_generator import PaymentQRGenerator


# Define admin users
ADMIN_USERS = ["1057935170", "987654321", "896838908"]  # Replace with actual Telegram user IDs

# Define user mappings
USER_ID_MAPPINGS = {
    "867015064": "naro",  # Telegram ID to username mapping for customer 1
    "964470824": "pong",  # Telegram ID to username mapping for customer 2
    "1130217514": "kheng"
}

# Function to check if a user is an admin
def is_admin(user_id):
    return str(user_id) in ADMIN_USERS

class PaymentBot:
    def __init__(self):
        """Initialize bot with required components."""
        self.qr_generator = PaymentQRGenerator()
        self.db = PaymentDatabase()

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        user_telegram_id = str(update.message.from_user.id)
        
        # Base welcome message for all users
        welcome_message = (
            "🎉 Welcome to ABA Digital Lending Payment Bot! 🤖\n\n"
            "Available Commands:\n"
            "➡️ /qr <user_id> <amount> - Generate payment QR code\n"
            "➡️ /recent - View last payment receipt\n"
            "➡️ /history - View your payment history\n"
            "➡️ /status - Check bot status\n"
        )
        
        # Add admin-only commands if user is admin
        if is_admin(user_telegram_id):
            welcome_message += (
                "Admin Commands:\n"
                "➡️ /history <user_id> - View payment history for any user\n"
                "➡️ /help - Show detailed help message\n\n"
                "Need help? Just type /help to see all commands!"
            )
        else:
            welcome_message += "\nContact @HelpCenter if you need assistance."
        
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command - restricted to admins only."""
        user_telegram_id = str(update.message.from_user.id)
        
        # Check if user is an admin
        if is_admin(user_telegram_id):
            help_message = (
                "📚 Command Guide:\n\n"
                "1️⃣ Generate Payment QR:\n"
                "   /qr <user_id> <amount>\n"
                "   Example: /qr john123 50.50\n\n"
                "2️⃣ View Payment Receipt:\n"
                "   /recent\n"
                "   Shows your last payment details\n\n"
                "3️⃣ Check Payment History:\n"
                "   /history [user_id]\n"
                "   - Use without user_id to see your own history\n"
                "   - Admins can specify user_id to see others\n\n"
                "4️⃣ Check Bot Status:\n"
                "   /status\n"
                "   Shows current bot status\n\n"
                "❓ Need more help? Contact @Mony_Pong"
            )
            await update.message.reply_text(help_message)
        else:
            await update.message.reply_text(
                "❌ Access Denied!\n"
                "Only administrators can access the help command."
            )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command."""
        user_telegram_id = str(update.message.from_user.id)
        
        # Check if user is admin or registered customer
        if not (is_admin(user_telegram_id) or user_telegram_id in USER_ID_MAPPINGS):
            await update.message.reply_text(
                "❌ Access Denied!\n"
                "You are not authorized to check bot status."
            )
            return

        db_status = "✅ Connected" if self.db.ensure_connection() else "❌ Disconnected"
        status_message = (
            "🔄 System Status\n"
            "══════════════\n\n"
            f"🤖 Bot: ✅ Online\n"
            f"🗄️ Database: {db_status}\n"
            f"🌐 QR Service: ✅ Available\n"
            f"🕒 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            "All systems operational! 👍"
        )
        await update.message.reply_text(status_message)

    async def history_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /history command with both admin and user access."""
        user_telegram_id = str(update.message.from_user.id)
        
        # If user is admin and provides a user ID, show that user's history
        if is_admin(user_telegram_id) and context.args:
            requested_user_id = context.args[0]
            history = self.db.get_user_history(requested_user_id)
        # If user is a registered customer, show their own history
        elif user_telegram_id in USER_ID_MAPPINGS:
            requested_user_id = USER_ID_MAPPINGS[user_telegram_id]
            history = self.db.get_user_history(requested_user_id)
        # If user is neither admin nor registered customer
        else:
            await update.message.reply_text(
                "❌ Access Denied!\n"
                "You are not authorized to view payment history."
            )
            return

        if history:
            message = f"📊 Payment History: {requested_user_id}\n══════════════\n\n"
            total_amount = 0

            for payment in history:
                amount = float(payment['amount'])
                total_amount += amount

                message += (
                    f"🔸 Transaction #{payment['id']}\n"
                    f"💰 Amount: ${amount:.2f}\n"
                    "──────────\n"
                )

            message += (
                f"\n💵 Total Payments: ${total_amount:.2f}\n"
                f"📊 Total Transactions: {len(history)}"
            )
            await update.message.reply_text(message)
        else:
            await update.message.reply_text(
                f"❌ No payment history found for {requested_user_id}\n"
                "Make sure the user ID is correct and try again."
            )

    async def create_qr_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /qr command."""
        user_telegram_id = str(update.message.from_user.id)
        
        # Check if user is admin or registered customer
        if not (is_admin(user_telegram_id) or user_telegram_id in USER_ID_MAPPINGS):
            await update.message.reply_text(
                "❌ Access Denied!\n"
                "You are not authorized to generate QR codes."
            )
            return

        try:
            if len(context.args) != 2:
                await update.message.reply_text(
                    "⚠️ Invalid format!\n"
                    "Correct usage: /qr <user_id> <amount>\n"
                    "Example: /qr john123 50.50"
                )
                return

            user_id, amount = context.args
            
            if not self.qr_generator.validate_user_id(user_id):
                await update.message.reply_text(
                    "❌ Invalid user ID!\n"
                    "User ID should be 4-20 characters long and contain\n"
                    "only letters, numbers, underscores, or hyphens."
                )
                return

            try:
                amount = amount.replace('$', '').strip()
                amount_float = float(amount)
                if amount_float <= 0 or amount_float > Config.MAX_AMOUNT:
                    await update.message.reply_text(
                        f"❌ Invalid amount!\n"
                        f"Amount must be between $0 and ${Config.MAX_AMOUNT}"
                    )
                    return
            except ValueError:
                await update.message.reply_text(
                    "❌ Invalid amount!\n"
                    "Please enter a valid number."
                )
                return

            if not self.db.store_payment(user_id, amount_float):
                await update.message.reply_text(
                    "❌ Failed to process payment.\n"
                    "Please try again later."
                )
                return

            await update.message.reply_text("🔄 Generating payment QR code...")
            payment_info = f"{Config.PAYMENT_BASE_URL}?user={user_id}&amount={amount_float}"
            qr_image = self.qr_generator.generate_qr_code(payment_info)

            if qr_image:
                logger.info(f"Generated QR code for user {user_id} with amount ${amount_float}")
                await update.message.reply_photo(
                    photo=InputFile(qr_image, filename="payment_qr.png"),
                    caption=(
                        "🎉 Payment QR Code Generated!\n"
                        "══════════════\n"
                        f"👤 User ID: {user_id}\n"
                        f"💰 Amount: ${amount_float:.2f}\n"
                        f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"🔗 Payment Link:{payment_info}\n\n"
                        " ℹ️ Use /recent to view payment receipt\n"
                        "💡 Scan QR code to complete payment"
                    )
                )
            else:
                await update.message.reply_text(
                    "❌ Failed to generate QR code.\n"
                    "Please try again later."
                )

        except Exception as e:
            logger.error(f"Error in create_qr_command: {str(e)}")
            await update.message.reply_text(
                "❌ An error occurred.\n"
                "Please try again later."
            )

    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /recent command to show payment receipt."""
        user_telegram_id = str(update.message.from_user.id)
        
        # If user is admin, show the latest payment
        if is_admin(user_telegram_id):
            latest_payment = self.db.get_latest_payment()
        # If user is a registered customer, show their own latest payment
        elif user_telegram_id in USER_ID_MAPPINGS:
            user_id = USER_ID_MAPPINGS[user_telegram_id]
            latest_payment = self.db.get_user_latest_payment(user_id)
        # If user is neither admin nor registered customer
        else:
            await update.message.reply_text(
                "❌ Access Denied!\n"
                "You are not authorized to view payment receipts."
            )
            return

        if latest_payment:
            amount = float(latest_payment['amount'])
            receipt_message = (
                "🧾 Payment Receipt\n"
                "══════════════\n"
                f"📝 Transaction ID: #{latest_payment['id']}\n"
                f"👤 User ID: {latest_payment['userid']}\n"
                f"💰 Amount Paid: ${amount:.2f}\n"
                f"🕒 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"✅ Status: Payment Successful\n\n"
                "Thank you for your payment! 🙏\n"
                "══════════════\n\n"
                "Need help? Contact an administrator."
            )
            await update.message.reply_text(receipt_message)
        else:
            await update.message.reply_text(
                "❌ No recent payments found\n"
                "Use /qr to make a payment first."
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors in the bot."""
        logger.error(f"Update {update} caused error {context.error}")
        
        error_message = (
            "❌ An error occurred while processing your request.\n"
            "Please try again later or contact support if the issue persists."
        )
        
        if update and update.message:
            await update.message.reply_text(error_message)