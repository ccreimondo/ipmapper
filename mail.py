#!/usr/bin/env python

def send_email(subject, text):
    import smtplib
    from secret import gmail, server, reimondo

    gmail_user = gmail.ID
    gmail_pwd = gmail.PWD
    FROM = server.MAIL
    TO = [reimondo.QQMAIL]  # Must be a list
    SUBJECT = subject
    TEXT = text

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # server_ssl.ehlo() # optional, called by login()
        server_ssl.login(gmail_user, gmail_pwd)
        server_ssl.sendmail(FROM, TO, message)
        server_ssl.close()
        print "successfully sent the mail"
    except:
        print "Fail"


def test():
    send_email("Test", "Test send mail from server with gmail")


if __name__ == "__main__":
    test()
