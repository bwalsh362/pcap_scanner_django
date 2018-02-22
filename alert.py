import smtplib


def send_alert(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("bwalsh362@gmail.com", "Charlie362")
    server.sendmail("bwalsh362@gmail.com", "brianmx362@hotmail.com", msg)
    server.quit()
