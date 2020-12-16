from email.mime.text import MIMEText
import smtplib

def send_email(email, height, average_height, count):
    from_email="<you_email>"
    from_password="<passw>"
    to_email = email

    subject="Height data!"
    message=f"You heigh is <strong>{height}</strong>.<br>Avarage height of all persons is <strong>{average_height}</strong><br> Count of reports is: {count}<br> Thank you!"

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=email
    msg['From']=from_email

    gmail=smtplib.SMTP_SSL('mail.inbox.lv', 465) #creates SSL conection
    gmail.ehlo()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
    gmail.quit()