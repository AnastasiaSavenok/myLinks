import os
import smtplib

from config.settings import EMAIL_ADDRESS, EMAIL_PASSWORD


def sending_mail(user, token):
    host = EMAIL_ADDRESS
    password = EMAIL_PASSWORD
    subject = "Код подтверждения"
    to = user
    charset = 'Content-Type: text/plain; charset=utf-8'
    mime = 'MIME-Version: 1.0'
    text = f"Verify code: {token}"
    body = "\r\n".join((f"From: {host}", f"To: {to}",
                        f"Subject: {subject}", mime, charset, "", text))

    try:
        smtp = smtplib.SMTP(host='smtp.gmail.com', port=587)
        smtp.starttls()
        smtp.ehlo()
        smtp.login(host, password)
        smtp.sendmail(host, user, body.encode('utf-8'))
    except smtplib.SMTPException as err:
        raise err
    finally:
        smtp.quit()
