import imaplib
import email
import time
import os

# Email credentials and server settings
EMAIL = ''
PASSWORD = 'aonw bgjg rsjp szay'
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

# Function to check for new emails
def check_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')

        # Search for unseen emails
        result, data = mail.search(None, 'UNSEEN')
        
        if result == 'OK':
            email_ids = data[0].split()
            for email_id in email_ids:
                result, email_data = mail.fetch(email_id, '(RFC822)')
                if result == 'OK':
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    subject = msg['subject']
                    sender = msg['from']
                    # Notify the user about the new email
                    os.system('osascript -e \'display notification "New Email" with title "{}" subtitle "{}"\''.format(subject, sender))

        mail.close()
        mail.logout()
    except Exception as e:
        print("Error:", e)

# Main loop to check for new emails every minute
if __name__ == "__main__":
    while True:
        check_emails()
        time.sleep(10)  # Check every minute
