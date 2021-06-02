from django.core import mail


import threading


class EmailThread(threading.Thread):

    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def run(self):
        with mail.get_connection() as connection:
            mail.EmailMessage(
                subject=self.data['email_subject'], body=self.data['email_body'], to=[self.data['to_email']],
                connection=connection,
            ).send()


class MailSenderUtil:
    @staticmethod
    def send_email(data):
        EmailThread(data).start()
