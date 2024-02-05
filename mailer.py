from config import HOST, USERNAME, PASSWORD, PORT, MailBody
from smtplib import SMTP_SSL


def send_mail(data: dict):
    msg = MailBody(**data)

    try:
        server_ssl = SMTP_SSL(HOST, int(PORT))
        server_ssl.login(USERNAME, PASSWORD)
        server_ssl.sendmail(USERNAME, msg.to, msg.body)
        server_ssl.close()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": e}
