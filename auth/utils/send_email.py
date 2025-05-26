import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, Template


load_dotenv()


def send_mail(email: str, subject: str,fullName: str, confirmation_link: str, template_path: str):
    """
    Send an email using SMTP.
    """

    # SMTP server configuration
    smtp_server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("SMTP_PORT"))
    username = os.getenv("MAILMUG_USERNAME")
    password = os.getenv("MAILMUG_PASSWORD")
    print(smtp_server, port, username, password)
    # Email details
    sender_email = "devgentlesoul18@gmail.com"
    to_email = email
    
    # Load the HTML template
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_path)

    html = template.render(
        fullName=fullName,
        confirmation_link=confirmation_link
    )
    html_content = html

    # Create the email message
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = to_email

    # Attach the HTML content
    part = MIMEText(html_content, 'html')
    message.attach(part)

    # Send the email
    with smtplib.SMTP(smtp_server, port) as server:
        server.set_debuglevel(1)
        server.esmtp_features['auth'] = 'LOGIN PLAIN'
        server.login(username, password)
        server.sendmail(sender_email, to_email, message.as_string())
    return True
# port = 2525
# smtp_server = "smtp.mailmug.net"
# password = os.getenv("MAILMUG_PASSWORD")
# username = os.getenv("MAILMUG_USERNAME")

# sender_email = "devgentlsoul18@gmail.com"
# to_email = "email"

# message = MIMEMultipart('alternative')
# message['Subject'] = "Test Email"
# message['From'] = sender_email
# message['To'] = to_email
# html = "html"
# part = MIMEText(html, 'html')
# message.attach(part)

# server = smtplib.SMTP(smtp_server, port)
# server.set_debuglevel(1)
# server.esmtp_features['auth'] = 'LOGIN PLAIN'
# server.login(username, password)
# server.sendmail(sender_email, to_email, message.as_string())
