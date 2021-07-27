import traceback
from typing import Optional
from django.core.mail import EmailMessage
from utils.logger import Logger
from utils.exception import CustomException


def send_mail(from_email: str, recipients: list, subject: str, body: str, extra_data: Optional[dict] = None):
    try:
        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=recipients
        )
        email.send()
    except Exception as error:
        error_msg = traceback.format_exc()
        Logger.error(error_msg)
        raise CustomException(
            title="Could not send exception",
            detail=error_msg
        )
