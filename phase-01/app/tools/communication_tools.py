from ..logs.execution_logger import ExecutionLogger

class CommunicationTools:
    @staticmethod
    async def send_email(to_email: str, subject: str, body: str) -> bool:
        ExecutionLogger.log("Communication", f"Sending email to {to_email}", f"Subject: {subject}")
        # In a real app, this would use SMTP or an API
        return True

    @staticmethod
    async def send_whatsapp_message(phone: str, message: str) -> bool:
        ExecutionLogger.log("Communication", f"Sending WhatsApp to {phone}", f"Message: {message[:20]}...")
        return True
