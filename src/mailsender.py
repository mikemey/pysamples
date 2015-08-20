import os
from smtplib import SMTP

from email.mime.text import MIMEText

from mlc_commons import logger


def send(email_subject, email_content):
    server_set = 'DRC_SMTP_SERVER' in os.environ
    if not server_set:
        logger.error("email variables not set!")
        return 1

    smtp_server = os.environ['DRC_SMTP_SERVER']
    sender = os.environ['DRC_SENDER']
    destination = [os.environ['DRC_DESTINATION']]

    username = os.environ['DRC_USERNAME']
    password = os.environ['DRC_PASSWORD']

    try:
        text_subtype = 'html'
        msg = MIMEText(email_content, text_subtype)
        msg['Subject'] = email_subject
        msg['From'] = sender

        conn = SMTP(smtp_server)
        conn.set_debuglevel(False)
        conn.login(username, password)
        try:
            logger.info('sending mail....')
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            conn.close()
            return 0
    except Exception, exc:
        # sys.exit( "mail failed; %s" % str(exc) ) # give a error message
        logger.info('sending failed: %s' % str(exc))
        return 1