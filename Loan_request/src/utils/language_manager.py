class LanguageManager:
    MESSAGES = {
    'english': {
        'select_language': "🌐 *Step 0:*\nPlease choose your language:",
        'user_status_prompt': "Are you a new user? Please select an option:",
        'new_user': "Yes, I'm new",
        'existing_user': "No, I'm returning",
        'auth_prompt': "🔐 *Step 0.5:*\nPlease enter your 6‑digit PIN or your Telegram ID (i you forgot your PIN).",
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
        'repayment_details': ("✅ *Repayment Details:*\n\n"
                              "• Total Repayment: ${total_repayment:.2f}\n"
                              "• Installments: {installments}\n"
                              "• Frequency: {frequency}\n\n"
                              "{schedule_text}\n\n"
                              "💡 Please ensure timely payments."),
        'repayment_ack': "👍 *Step 12:*\nThanks for confirming the repayment schedule.\nWould you like a detailed loan report?",
        'report_sent': "📄 *Step 13:*\nYour report has been sent and reminders scheduled. Thank you for choosing Loan Lending!",
        'assist_options': "How may we assist you further? Please choose an option:",
        'setid_prompt': "📸 Please upload a clear image of your National ID for secure extraction and storage.",
        'setid_success': "✅ Your National ID has been set successfully for future pre‑approval.",
        'setpin_prompt': ("🔐 For security, please set your 6‑digit PIN.\n"
                          "If you are updating your PIN, please first enter your current PIN via /setpin.\n"
                          "Enter your desired 6‑digit PIN:"),
        'setpin_success': "✅ Your PIN has been set successfully!\nYour Telegram ID is: {telegram_id}\nKeep it safe—you will need it to authenticate.",
        'report_title': "📄 *Your Detailed Loan Report*",
        'i_understand': "I Understand",
        'cancel': "Cancel",
        # File upload messages
        'invalid_signature': "⚠️ The uploaded image does not appear to be a valid digital signature. Please try again.",
        'error_encrypting_signature': "⚠️ Error encrypting signature. Please try again.",
        'invalid_file_type': "⚠️ Please upload a valid document or photo.",
        'selfie_must_be_photo': "⚠️ Please upload a photo for your selfie, not a document.",
        'upload_error': "⚠️ There was an error uploading your file. Please try again."
    },
    'khmer': {
        'select_language': "🌐 *ជំហាន ០:*\nសូមជ្រើសរើសភាសារបស់អ្នក៖",
        'user_status_prompt': "តើអ្នកជាអ្នកប្រើថ្មីឬ? សូមជ្រើសរើសជម្រើសមួយ៖",
        'new_user': "បាទ/ចាស, ខ្ញុំជាអ្នកប្រើថ្មី",
        'existing_user': "ទេ, ខ្ញុំបានប្រើរួចហើយ",
        'auth_prompt': "🔐 *ជំហាន ០.៥:*\nសូមវាយលេខ PIN 6 ខ្ទង់ ឬ Telegram ID (បើភ្លេច PIN) សម្រាប់ផ្ទៀងផ្ទាត់។",
        'set_pin_required': "⚠️ សម្រាប់សុវត្ថិភាព អ្នកត្រូវកំណត់លេខ PIN 6 ខ្ទង់ ជាមុន ដោយ /setpin\nTelegram ID របស់អ្នក: {telegram_id}",
        'auth_success': "✅ ផ្ទៀងផ្ទាត់ជោគជ័យ។",
        'auth_success_with_id': "Telegram ID របស់អ្នក: {telegram_id}",
        'auth_success_by_id': "✅ ផ្ទៀងផ្ទាត់ជោគជ័យដោយប្រើ Telegram ID។",
        'incorrect_pin': "❌ លេខ PIN មិនត្រឹមត្រូវ។ សូមព្យាយាមម្ដងទៀត។",
        'incorrect_auth': "❌ លេខ PIN ឬ Telegram ID មិនត្រឹមត្រូវ។ សូមព្យាយាមម្ដងទៀត។",
        'preapproval_prompt': "🔑 *ការអនុម័តជាមុន:*\nសូមវាយលេខអនុម័តជាមុនរបស់អ្នក៖",
        'preapproval_found': "✅ អនុម័តជាមុនផ្ទៀងផ្ទាត់បាន! កំពុងបន្តដាក់ពាក្យឥណទាន។",
        'preapproval_not_found': "❌ លេខអនុម័តជាមុន ឬ PIN មិនត្រឹមត្រូវ។ សូមពិនិត្យព័ត៌មានរបស់អ្នក។",
        'preapproval_id_message': "🔑 *លេខអនុម័តជាមុនរបស់អ្នក*: {preapproval_id}\nសូមរក្សាទុកលេខនេះឲ្យមានសុវត្ថិភាព សម្រាប់ដាក់ពាក្យឥណទានយ៉ាងរហ័ស។",
        'welcome': "👋 *ជំហាន ១:*\nសូមស្វាគមន៍មកកាន់ Loan Lending!\nដំណើរការផ្តល់ឥណទានចាប់ផ្តើមនៅទីនេះ។",
        'select_tenor': "📌 *ជំហាន ២:*\nសូមជ្រើសរើសរយៈពេលឥណទានរបស់អ្នក៖",
        'tenor_options': ["២ សប្តាហ៍ 🗓️", "១ ខែ 🗓️", "២ ខែ 🗓️"],
        'select_amount': "✅ *ជំហាន ៣:*\nអ្នកបានជ្រើសរើស *{tenor}*។\nសូមជ្រើសចំនួនប្រាក់ឥណទានដែលអ្នកចង់បាន៖",
        'amount_prompt': "💰 សូមជ្រើសចំនួនប្រាក់៖",
        'loan_amounts': [50, 75, 100, 120, 150, 175, 200],
        'upload_doc': "📄 *ជំហាន ៤:*\nចំនួនប្រាក់: *${amount}*។\nសូមផ្ទុកឡើងប័ណ្ណប្រាក់ខែឬកាតការិយាល័យសម្រាប់ផ្ទៀងផ្ទាត់។",
        'file_too_large': "⚠️ ឯកសារធំនេះធំពេក! សូមផ្ទុកឡើងឯកសារតិចជាង 10MB ឬវាយ /cancel។",
        'doc_received': "✅ ឯកសារទទួលបាន!\nសូមផ្ទុកឡើងអត្តសញ្ញាណជាតិរបស់អ្នក។",
        'upload_id': "🆔 អត្តសញ្ញាណជាតិទទួលបាន!\nកំពុងយកអត្តសញ្ញាណជាតិ...",
        'id_confirm_prompt': "យើងបានរកឃើញអត្តសញ្ញាណជាតិ៖ *{national_id}*\nតើនេះត្រឹមត្រូវទេ?",
        'id_confirmed': "✅ អត្តសញ្ញាណជាតិផ្ទៀងផ្ទាត់បាន! សូមបន្តផ្ទុកឡើងរូបថតផ្ទាល់ខ្លួន។",
        'upload_selfie': "📸 សូមផ្ទុកឡើងរូបថតផ្ទាល់ខ្លួនសម្រាប់ផ្ទៀងផ្ទាត់មុខ។",
        'selfie_verified': "✅ រូបថតផ្ទាល់ខ្លួនផ្ទៀងផ្ទាត់បាន! សូមផ្តល់ព័ត៌មានការងារ (ចាប់ផ្តើមពីរយៈពេលការងារ)។",
        'factory_workers': "👥 ចំនួនបុគ្គលិក (ប្រមាណ):",
        'factory_locations': "🏭 ចំនួនទីតាំងរោងចក្រ:",
        'factory_origin': "🌎 ប្រភពរោងចក្រ (ប្រទេស):",
        'eligibility_prompt': "⏳ កំពុងគណនាពិន្ទុឥណទានរបស់អ្នក...",
        'eligibility_result': "ពិន្ទរបស់អ្នកគឺ *{score:.2f}* ({status})។ អ្នកអាចមានសមត្ថភាពឥណទានដល់ *${loan_amount}*។\nតើបន្តទេ?",
        'confirm_buttons': {"confirm": "បន្ត", "cancel": "បោះបង់"},
       'review_details': (
    "🔍 *ជំហាន ៨:*\nពិនិត្យព័ត៌មានការងាររបស់អ្នក៖\n\n"
    "• រយៈពេលការងារ: {work_duration} ខែ\n"
    "• ចំនួនកម្មករ: {factory_workers}\n"
    "• ចំនួនទីតាំងរោងចក្រ: {factory_locations}\n"
    "• ប្រភពរោងចក្រ: {factory_origin}\n\n"
    "តើនេះត្រឹមត្រូវទេ?"
),

        'agreement': "✍️ *ជំហាន ៩:*\nតើអ្នកយល់ព្រមលើលក្ខខណ្ឌឥណទានទេ? (បាទ/ចាស\tទេ)",
        'loan_cancelled': "❌ ការដាក់ពាក្យឥណទានត្រូវបានបោះបង់។ វាយ /start ដើម្បីចាប់ផ្តើមឡើងវិញ។",
        'contract_text': (
            "*កិច្ចសន្យាឥណទាន*\n\n"
            "កិច្ចសន្យានេះគឺរវាង *Loan Lending* និង *{full_name}* នៅថ្ងៃទី {timestamp}។\n\n"
            "*ព័ត៌មានឥណទាន:*\n"
            "• ចំនួនប្រាក់: ${amount}\n"
            "• រយៈពេល: {tenor}\n"
            "• សេវាកម្មដំណើរការ: $5\n"
            "• ប្រាក់រប្រាក់សរុប: ${interest}\n\n"
            "*ព័ត៌មានការងារ:*\n"
            "• រយៈពេលការងារ: {work_duration} ខែ\n"
            "• ចំនួនកម្មករ: {factory_workers}\n"
            "• ចំនួនទីតាំងរោងចក្រ: {factory_locations}\n"
            "• ប្រភពរោងចក្រ: {factory_origin}\n\n"
            "*ព័ត៌មានការទូទាត់:*\n"
            "• ចំនួនទូទាត់សរុប: ${total_repayment}\n\n"
            "*លក្ខខណ្ឌ:*\n"
            "1. អាស្រ័យលើការផ្ទៀងផ្ទាត់របស់ធនាគារ។\n"
            "2. ប្រាក់រប្រាក់ 5% ត្រូវបានអនុវត្តក្នុងរៀងរាល់កាលកំណត់។\n"
            "3. ដោយការចុះហត្ថលេខា អ្នកបញ្ជាក់ថាព័ត៌មានទាំងអស់ត្រឹមត្រូវ។\n"
            "4. អាចមានកម្រៃពិន័យពេលយឺតការទូទាត់។\n\n"
            "សូមចុះហត្ថលេខាដោយផ្ទុកឡើងហត្ថលេខាឌីជីថលខាងក្រោម។"
        ),
        'upload_signature': "🖊 *ជំហាន ១០:*\nសូមផ្ទុកឡើងហត្ថលេខាឌីជីថលរបស់អ្នក ដើម្បីបញ្ចប់កិច្ចសន្យា។",
        'signature_received': "✅ ហត្ថលេខាត្រូវបានទទួល និងផ្ទៀងផ្ទាត់បាន! ឥណទានរបស់អ្នកត្រូវបានអនុម័ត។\n\n*ជំហាន ១១:*\nសូមជ្រើសរើសកាលវិភាគការទូទាត់។",
        'select_schedule': "📆 សូមជ្រើសរើសកាលវិភាគការទូទាត់៖",
        'schedule_options': ["ប្រចាំសប្តាហ៍", "ប្រចាំពីសប្តាហ៍", "ប្រចាំខែ"],
        'repayment_details': ("✅ *ព័ត៌មានការទូទាត់:*\n\n"
                              "• ចំនួនទូទាត់សរុប: ${total_repayment:.2f}\n"
                              "• លេខកង់: {installments}\n"
                              "• ប្រចាំ: {frequency}\n\n"
                              "{schedule_text}\n\n"
                              "💡 សូមធ្វើការទូទាត់ឲ្យទាន់ពេល។"),
        'repayment_ack': "👍 *ជំហាន ១២:*\nសូមអរគុណដែលបានផ្ទៀងផ្ទាត់កាលវិភាគការទូទាត់។ តើអ្នកចង់បានរបាយការណ៍លម្អិតទេ?",
        'report_sent': "📄 *ជំហាន ១៣:*\nរបាយការណ៍បានផ្ញើហើយ កាលវិភាគរំលឹកត្រូវបានកំណត់។ សូមអរគុណដែលបានជ្រើស Loan Lending!",
        'assist_options': "តើយើងអាចជួយអ្នកបន្ថែមយ៉ាងដូចម្ដេច? សូមជ្រើសរើសជម្រើសមួយ៖",
        'setid_prompt': "📸 សូមផ្ទុកឡើងរូបភាពច្បាស់នៃអត្តសញ្ញាណជាតិ ដើម្បីយកនិងរក្សាទុកដោយសុវត្ថិភាព។",
        'setid_success': "✅ អត្តសញ្ញាណជាតិរបស់អ្នកបានកំណត់ដោយជោគជ័យ សម្រាប់ការអនុម័តជាមុនក្រោយៗ។",
        'setpin_prompt': ("🔐 សម្រាប់សុវត្ថិភាព សូមវាយលេខ PIN 6 ខ្ទង់ ដែលអ្នកបានកំណត់រួចហើយ (បើចង់ធ្វើបច្ចុប្បន្នភាព សូមប្រើ /setpin)។\n"
                          "បើអ្នកចង់កំណត់លេខ PIN ថ្មី សូមប្រើ /setpin។"),
        'setpin_success': "✅ លេខ PIN របស់អ្នកត្រូវបានកំណត់ឡើងដោយជោគជ័យ!\nTelegram ID របស់អ្នក: {telegram_id}\nសូមរក្សាទុកវាឲ្យមានសុវត្ថិភាព។",
        'report_title': "📄 *របាយការណ៍ឥណទានលម្អិតរបស់អ្នក*",
        'i_understand': "ខ្ញុំយល់",
        'cancel': "បោះបង់",
        # Digital signature additional keys:
        'invalid_signature': "⚠️ រូបភាពដែលបានផ្ទុកឡើងមិនមែនជាហត្ថលេខាត្រឹមត្រូវទេ។ សូមព្យាយាមផ្ទុកឡើងម្ដងទៀត។",
        'error_encrypting_signature': "⚠️ មានបញ្ហាក្នុងការបំលែងឯកសារ។ សូមព្យាយាមម្ដងទៀត។"
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