################################
#Fichero: correo.py
#Descripción: Fichero que nos permite enviar el
#             correo electronico.
################################

# Librerias utilizadas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

################################
#Función: email
#Descripción: Envia el correo electronico para la informaciónSNMP.             
#Parámetros: user (usuario que solicita la información)                         
################################
def email(user):
    sender_email_address = 'correo@correo.com'
    sender_email_password = 'contraseña'
    if user['id'] == CODIGOUSUARIO1:
        receiver_email_address = 'correo@correo.com'
    elif user['id'] == CODIGOUSUARIO2:
        receiver_email_address = 'correo@correo.com'
        
    email_subject_line = 'Información SNMP'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Información solicitada mediante el bot de telegram.'
    msg.attach(MIMEText(email_body, 'plain'))

    # Adjuunta PDF informacionSNMP
    filename = 'infoSNMP.pdf'
    attachment_file = open('infoSNMP.pdf', 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment_file).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment_file; filename = "+filename)

    #Adjunta PDF con log de usuarios
    filename2 = 'LogUsers.pdf'
    attachment_file2 = open('LogUsers.pdf', 'rb')
    part2 = MIMEBase('application', 'octet-stream')
    part2.set_payload((attachment_file2).read())
    encoders.encode_base64(part2)
    part2.add_header('Content-Disposition', "attachment_file2; filename = "+filename2)

    msg.attach(part)
    msg.attach(part2)
    print('Ficheros adjuntos')
    email_body_content = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email_address, sender_email_password)
    server.sendmail(sender_email_address, receiver_email_address, email_body_content)
    server.quit()

################################
#Función: email
#Descripción: Envia el correo electronico para notificar el TRAP.             
#Parámetros: No tiene.                         
################################
def emailprocesos():
    sender_email_address = 'correo@correo.com'
    sender_email_password = 'contraseña'
    receiver_email_address = 'correo@correo.com'

    email_subject_line = 'TRAP Generado'

    msg = MIMEMultipart()
    msg['From'] = sender_email_address
    msg['To'] = receiver_email_address
    msg['Subject'] = email_subject_line

    email_body = 'Trap generado. Se ha superado el número de procesos permitidos.\nSe muestran los procesos actuales:'
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
    #server.sendmail(sender_email_address, receiver_email_address_2, email_body_content)
    server.quit()
