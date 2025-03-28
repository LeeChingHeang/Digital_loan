import logging
import datetime
from telegram.ext import CallbackContext

logger = logging.getLogger(__name__)

class ReminderService:
    @staticmethod
    async def reminder_callback(context: CallbackContext) -> None:
        """Callback function for sending scheduled reminders"""
        job = context.job
        data = job.data
        chat_id = data['chat_id']
        message = data['message']
        
        logger.info(f"Sending reminder to chat {chat_id}: {message}")
        await context.bot.send_message(chat_id=chat_id, text=message)

    @staticmethod
    def schedule_reminders(context: CallbackContext, chat_id: int, installments_list: list) -> None:
        """
        Schedule payment reminders for each installment
        
        Args:
            context: The callback context
            chat_id: The chat ID to send reminders to
            installments_list: List of installment details
        """
        now = datetime.datetime.now()
        
        for installment in installments_list:
            installment_number = installment['installment']
            amount = installment['amount']
            due_date = installment['due_date']

            # Calculate reminder dates relative to the due date
            reminder_dates = [
                due_date - datetime.timedelta(days=7),  # 1 week before
                due_date - datetime.timedelta(days=1),  # 1 day before
                due_date,                               # On due date
                due_date + datetime.timedelta(days=1)   # 1 day after (overdue)
            ]

            # For demo/testing purposes, use short intervals
            test_offsets = [
                now + datetime.timedelta(seconds=10),
                now + datetime.timedelta(seconds=20),
                now + datetime.timedelta(seconds=30),
                now + datetime.timedelta(seconds=40)
            ]

            messages = [
                f"🔔 Reminder: Installment {installment_number} of ${amount:.2f} is due in 1 week.",
                f"🔔 Reminder: Installment {installment_number} of ${amount:.2f} is due tomorrow.",
                f"📅 Today is the due date for installment {installment_number} (${amount:.2f}).",
                f"⚠️ Alert: Installment {installment_number} of ${amount:.2f} is overdue."
            ]

            # Schedule reminders
            # In production, use reminder_dates instead of test_offsets
            for offset, message in zip(test_offsets, messages):
                context.job_queue.run_once(
                    ReminderService.reminder_callback,
                    offset,
                    data={'chat_id': chat_id, 'message': message}
                )

        logger.info(f"Reminders scheduled for {len(installments_list)} installment(s).")

    @staticmethod
    def cancel_reminders(context: CallbackContext, chat_id: int) -> None:
        """
        Cancel all scheduled reminders for a specific chat ID
        
        Args:
            context: The callback context
            chat_id: The chat ID whose reminders should be cancelled
        """
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in current_jobs:
            job.schedule_removal()
        logger.info(f"Cancelled all reminders for chat ID {chat_id}")

    @staticmethod
    def reschedule_reminder(context: CallbackContext, chat_id: int, 
                          installment_number: int, new_date: datetime.datetime) -> None:
        """
        Reschedule a specific reminder
        
        Args:
            context: The callback context
            chat_id: The chat ID
            installment_number: The installment number to reschedule
            new_date: The new due date
        """
        # Cancel existing reminders for this installment
        current_jobs = context.job_queue.get_jobs_by_name(f"{chat_id}_{installment_number}")
        for job in current_jobs:
            job.schedule_removal()

        # Schedule new reminders
        reminder_offsets = [
            datetime.timedelta(days=-7),  # 1 week before
            datetime.timedelta(days=-1),  # 1 day before
            datetime.timedelta(days=0),   # On due date
            datetime.timedelta(days=1)    # 1 day after
        ]

        messages = [
            f"🔔 Reminder: Rescheduled installment {installment_number} is due in 1 week.",
            f"🔔 Reminder: Rescheduled installment {installment_number} is due tomorrow.",
            f"📅 Today is the due date for rescheduled installment {installment_number}.",
            f"⚠️ Alert: Rescheduled installment {installment_number} is overdue."
        ]

        for offset, message in zip(reminder_offsets, messages):
            reminder_date = new_date + offset
            if reminder_date > datetime.datetime.now():
                context.job_queue.run_once(
                    ReminderService.reminder_callback,
                    reminder_date,
                    data={'chat_id': chat_id, 'message': message},
                    name=f"{chat_id}_{installment_number}"
                )

        logger.info(f"Rescheduled reminders for installment {installment_number}")