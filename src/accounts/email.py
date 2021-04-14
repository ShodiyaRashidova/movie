from threading import Thread

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.reverse import reverse
from rest_framework_simplejwt.tokens import RefreshToken


class EmailThread(Thread):

    def __init__(self, email):
        self.email = email
        Thread.__init__(self)

    def run(self):
        self.email.send()


def get_email_verify_url(request, user):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relative_link = reverse('email-verify')
    return 'http://' + current_site + relative_link + "?token=" + str(token)


def send_verify_email(request, user):
    data = {
        'email_body': 'Hi  Use the link below to verify your email \n' + \
                      get_email_verify_url(request, user),
        'to_email': user.email,
        'email_subject': 'Verify your email'
    }
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'],
        to=[data['to_email']])
    EmailThread(email).start()


def get_reset_password_url(request, user):
    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    current_site = get_current_site(request=request).domain
    relative_link = reverse(
        'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

    return 'http://' + current_site + relative_link + "?redirect_url=" + \
           request.data.get('redirect_url')


def send_reset_password(request, user):
    data = {
        'email_body': 'Hello, \n Use link below to reset your password \n' +
                      get_reset_password_url(request, user),
        'to_email': user.email,
        'email_subject': 'Reset your password'}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'],
        to=[data['to_email']])
    EmailThread(email).start()


def send_order_info(user, order):
    data = {
        'email_body': f'Hello, {user.first_name} You booked {order.quantity} ticket(s)'
                      f' for {order.schedule.movie.title} film in '
                      f' {order.schedule.movie_date} {order.schedule.movie_time} ',
        'to_email': user.email,
        'email_subject': 'Oder info '}
    email = EmailMessage(
        subject=data['email_subject'], body=data['email_body'],
        to=[data['to_email']])
    EmailThread(email).start()
