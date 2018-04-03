import imaplib
import config
import email

class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.username, self.password)


    def get_email(self):
        self.mail.list()
        self.mail.select("inbox") # connect to inbox.
        result, data = self.mail.search(None, "ALL")

        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        result, data = self.mail.fetch(latest_email_id, "(RFC822)")
        raw_email = data[0][1] # here's the body, which is raw text of the whole email
        # including headers and alternate payloads
        raw_email_string = raw_email.decode('utf-8')

        msg = email.message_from_string(raw_email_string)

        body = ''

        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8')
                #print(body)

        #print(msg['From'])

        return [msg['From'], self.remove_non_text(body), latest_email_id]

    def remove_non_text(self, string):
        clean = string.replace('\n', '').replace('\r', '')
        return clean
