from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from project import settings
from django.utils.translation import ugettext as _


def send_message(request):

    if request.method == 'POST':
        email = request.POST['email']
        subject = request.POST['subject'] + ' From ' + email
        message = request.POST['message']

        send_mail(
            subject,
            message,
            email,
            [settings.EMAIL_HOST_USER],
        )
        messages.success(request, _('Your mail has been sent successfully !'))

    return render(request, 'contact/contact.html', {'title': _('Contact-us')})
