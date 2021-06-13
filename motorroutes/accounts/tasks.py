from django.core import mail

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from motorroutes.celery import app


# redis-server
# celery -A motorroutes worker --loglevel=debug --concurrency=4
@app.task
def send_verification_email(user_id, current_site):
    user = User.objects.get(id=user_id)
    refresh = RefreshToken.for_user(user)
    token = refresh.access_token

    relative_link = reverse('email-verification')
    abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
    email_body = 'Hi ' + user.username + \
                 ' Use the link below to verify your email \n' + abs_url
    data = {'email_body': email_body, 'to_email': user.email,
            'email_subject': 'Verify your email'}
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']],
            connection=connection,
        ).send()
    return data
