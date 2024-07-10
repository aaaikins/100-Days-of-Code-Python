import smtplib


def send_email(sender_email, app_password, recipient_email, message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=sender_email, password=app_password)
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=recipient_email,
            msg= f"Subject: Look Up👆\n\n{message}")
