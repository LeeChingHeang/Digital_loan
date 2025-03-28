class LanguageManager:
    MESSAGES = {
        'english': {
            'select_language': "🌐 *Step 0:*\nPlease choose your language:",
            'user_status_prompt': "Are you a new user? Please select an option:",
            'new_user': "Yes, I'm new",
            'existing_user': "No, I'm returning",
            'auth_prompt': "🔐 *Step 0.5:*\nPlease enter your 6‑digit PIN or your Telegram ID (if you forgot your PIN).",
            'set_pin_required': "⚠️ For security, you must set your 6‑digit PIN first using /setpin.\nYour Telegram ID is: {telegram_id}",
            'auth_success': "✅ Authentication successful.",
            'auth_success_with_id': "Your Telegram ID is: {telegram_id}",
            'auth_success_by_id': "✅ Authentication successful using your Telegram ID.",
            'incorrect_pin': "❌ Incorrect PIN. Please try again.",
            'incorrect_auth': "❌ Incorrect PIN or Telegram ID. Please try again.",
            'preapproval_prompt': "🔑 *Pre‑Approval:*\nPlease enter your Pre‑Approval ID:",
            'preapproval_found': "✅ Pre‑approval verified! Proceeding with your loan application.",
            'preapproval_not_found': "❌ The Pre‑Approval ID or PIN is incorrect. Please check your details.",
            'preapproval_id_message': "🔑 *Your Pre‑Approval ID*: {preapproval_id}\nKeep this ID secure for expedited future applications.",
            'welcome': "👋 *Step 1:*\nWelcome to Loan Lending!\nYour hassle‑free financing journey begins here.",
            'select_tenor': "📌 *Step 2:*\nChoose your loan tenure:",
            'tenor_options': ["2 Weeks 🗓️", "1 Month 🗓️", "2 Months 🗓️"],
            'select_amount': "✅ *Step 3:*\nYou chose *{tenor}*. Now select your desired loan amount:",
            'amount_prompt': "💰 Select loan amount:",
            'loan_amounts': [50, 75, 100, 120, 150, 175, 200],
            'upload_doc': "📄 *Step 4:*\nLoan amount: *${amount}*.\nPlease upload your payslip or office card for verification must be in (doc) format.",
            'file_too_large': "⚠️ File too large! Upload a file smaller than 10MB or type /cancel.",
            'doc_received': "✅ Document received!\nPlease upload your national ID/NSFF.",
            'upload_id': "🆔 ID received!\nExtracting your National ID...",
            'id_confirm_prompt': "We detected your National ID as: *{national_id}*\nIs this correct?",
            'id_confirmed': "National ID confirmed. Please proceed to upload your selfie.",
            'upload_selfie': "📸 Please upload a clear selfie for face verification.",
            'selfie_verified': "✅ Selfie verified successfully! Please provide your employment details (starting with employment duration in months).",
            'factory_workers': "👥 Number of Factory Workers (approx.):",
            'factory_locations': "🏭 Number of Factory Locations:",
            'factory_origin': "🌎 Factory Origin (Country):",
            'eligibility_prompt': "⏳ Calculating your loan eligibility...",
            'eligibility_result': "Your eligibility score is *{score:.2f}* ({status}). You may qualify for up to *${loan_amount}*.\nProceed?",
            'confirm_buttons': {"confirm": "Proceed", "cancel": "Cancel"},
            'review_details': (
                "🔍 *Step 8:*\nReview your employee details:\n\n"
                "• Employment Duration: {work_duration} months\n"
                "• Factory Workers: {factory_workers}\n"
                "• Factory Locations: {factory_locations}\n"
                "• Factory Origin: {factory_origin}\n\n"
                "Is this correct?"
            ),
            'agreement': "✍️ *Step 9:*\nDo you agree to the loan terms? (Yes/No)",
            'loan_cancelled': "❌ Loan application canceled. Type /start to begin again.",
            'contract_text': (
                "*Loan Agreement Contract*\n\n"
                "This contract is between *Loan Lending* and *{full_name}* on {timestamp}.\n\n"
                "*Loan Details:*\n"
                "• Amount: ${amount}\n"
                "• Tenor: {tenor}\n"
                "• Processing Charge: $5\n"
                "• Total Interest: ${interest}\n\n"
                "*Employment Details:*\n"
                "• Employment Duration: {work_duration} months\n"
                "• Factory Workers: {factory_workers}\n"
                "• Factory Locations: {factory_locations}\n"
                "• Factory Origin: {factory_origin}\n\n"
                "*Repayment Details:*\n"
                "• Total Repayment Amount: ${total_repayment}\n\n"
                "*Terms:*\n"
                "1. Subject to final bank verification.\n"
                "2. Fixed interest of 5% per period applies.\n"
                "3. By signing, you confirm all details are accurate.\n"
                "4. Late fees may apply.\n\n"
                "Please sign by uploading your digital signature below."
            ),
            'upload_signature': "🖊 *Step 10:*\nUpload your digital signature to finalize the contract.",
            'signature_received': "✅ Signature received and validated! Your loan is approved.\n\n*Step 11:*\nSelect your payment schedule.",
            'select_schedule': "📆 Select payment schedule:",
            'schedule_options': ["Weekly", "Bi‑Weekly", "Monthly"],
            'repayment_details': (
                "✅ *Repayment Details:*\n\n"
                "• Total Repayment: ${total_repayment:.2f}\n"
                "• Installments: {installments}\n"
                "• Frequency: {frequency}\n\n"
                "{schedule_text}\n\n"
                "💡 Please ensure timely payments."
            ),
            'repayment_ack': "👍 *Step 12:*\nThanks for confirming the repayment schedule.\nWould you like a detailed loan report?",
            'report_sent': "📄 *Step 13:*\nYour report has been sent and reminders scheduled. Thank you for choosing Loan Lending!",
            'assist_options': "How may we assist you further? Please choose an option:",
            'setid_prompt': "📸 Please upload a clear image of your National ID for secure extraction and storage.",
            'setid_success': "✅ Your National ID has been set successfully for future pre‑approval.",
            'setpin_prompt': (
                "🔐 For security, please set your 6‑digit PIN.\n"
                "If you are updating your PIN, please first enter your current PIN via /setpin.\n"
                "Enter your desired 6‑digit PIN:"
            ),
            'setpin_success': "✅ Your PIN has been set successfully!\nYour Telegram ID is: {telegram_id}\nKeep it safe—you will need it to authenticate.",
            'report_title': "📄 *Your Detailed Loan Report*",
            'i_understand': "I Understand",
            'cancel': "Cancel",
            'invalid_signature': "⚠️ The uploaded image does not appear to be a valid digital signature. Please try again.",
            'error_encrypting_signature': "⚠️ Error encrypting signature. Please try again."
        },
        'khmer': {
            # Khmer translations would go here, following the same structure
            # For brevity, I've omitted the Khmer translations, but they would mirror
            # the English structure with Khmer text
        }
    }

    @staticmethod
    def get_message(language: str, key: str, **kwargs) -> str:
        """
        Get a message in the specified language with optional formatting
        
        Args:
            language (str): The language code ('english' or 'khmer')
            key (str): The message key
            **kwargs: Format parameters for the message
            
        Returns:
            str: The formatted message in the specified language
        """
        try:
            message = LanguageManager.MESSAGES[language][key]
            if kwargs:
                return message.format(**kwargs)
            return message
        except KeyError:
            return f"Message not found: {key}"

    @staticmethod
    def get_button_text(language: str, key: str) -> str:
        """Get button text in the specified language"""
        try:
            return LanguageManager.MESSAGES[language]['confirm_buttons'][key]
        except KeyError:
            return key.capitalize()

    @staticmethod
    def get_options(language: str, key: str) -> list:
        """Get a list of options in the specified language"""
        try:
            return LanguageManager.MESSAGES[language][key]
        except KeyError:
            return []