from email.message import EmailMessage
import ssl
import smtplib
import creds


def sendMail(subject, body, html):
    email_sender = creds.email_sender
    email_password = creds.email_password
    email_receiver = creds.email_receiver

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    em.add_alternative(html, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print('Email sent')
        smtp.quit()
