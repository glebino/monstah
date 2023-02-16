import smtplib, ssl
from fileinput import filename

from envelope import Envelope
from pathlib import Path

def sendmail(filename):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "support@mydomain.com"
    receiver_email = ["glebino@mail.com", "glebino@mydomain.com"]
    #receiver_email = [
    #    "egor.prokhorenko@intrtl.com",
    #    "maxim.morozov@intrtl.com",
    #    "sergei.baramzin@intrtl.com",
    #    "olga.pilshchikova@intrtl.com"
    #]
    password = "ETk57wK91ETk57wK91"

    send_file = filename

    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)

    #email send zone

        Envelope()\
            .from_(sender_email)\
            .subject("Monthly stat report")\
            .to(receiver_email)\
            .message("")\
            .attach(Path(filename))\
            .smtp(smtp_server, port, sender_email, password)\
            .send()

        server.quit()
