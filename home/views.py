import smtplib
from email.mime.text import MIMEText

from django.core.mail import send_mail

from mysite.settings.base import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD


def enviar_correo():
    smtp_server = EMAIL_HOST
    smtp_port = 587
    smtp_username = EMAIL_HOST_USER
    smtp_password = EMAIL_HOST_PASSWORD

    # Create an email message
    message = MIMEText('This is a test email')
    message['Subject'] = 'Test Email'
    message['From'] = 'rodolfo@code43w.net'
    message['To'] = 'rodolfo@code43w.net'

    # Establish a connection to the SMTP server
    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()

    # Log in to the SMTP server
    smtp_connection.login(smtp_username, smtp_password)

    # Send the email
    smtp_connection.send_message(message)

    # Close the SMTP connection
    smtp_connection.quit()
