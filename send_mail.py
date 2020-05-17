import smtplib
from email.mime.text import MIMEText

def send_email(customer, rating, email, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '430f22cb08a528'
    password = 'c8de3480f91148'
    message = f'<h3>New feedback submission</h3><ul><li>Customer: {customer}</li><li>Rating: {rating}</li><li>email: {email}</li><li>comments: {comments}</li></ul>'

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'

    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    #SEND EMAIL
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


