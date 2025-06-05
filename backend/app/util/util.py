from werkzeug.security import generate_password_hash, check_password_hash
import requests
from datetime import datetime
import os
from flask import current_app

def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)

def _mailgun_send(subject: str, text: str) -> bool:
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    receiver = os.getenv("MAILGUN_RECEIVER")
    sender   = os.getenv("MAILGUN_SENDER")

    if not all([domain, api_key, receiver, sender]):
        current_app.logger.error("Mailgun: algumas variáveis de ambiente não estão definidas.")
        return False

    resp = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from":    sender,
            "to":      receiver,
            "subject": subject,
            "text":    text
        }
    )

    if not resp.ok:
        current_app.logger.error(f"Mailgun error [{resp.status_code}]: {resp.text}")
    return resp.ok