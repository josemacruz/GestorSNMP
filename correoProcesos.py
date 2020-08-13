import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email():
    sender_email_address = 'correo@correo.com'
    sender_email_password = 'contraseña'
    receiver_email_address = 'correo@correo.com'

    email_subject_line = 'Información Procesos'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Información solicitada mediante el bot de telegram.'
    msg.attach(MIMEText(email_body, 'plain'))

    filename = 'infoProcesos.pdf'
    attachment_file = open('infoProcesos.pdf', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment_file).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment_file; filename = "+filename)

    msg.attach(part)

    email_body_content = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email_address, sender_email_password)
    server.sendmail(sender_email_address, receiver_email_address, email_body_content)
    server.quit()
