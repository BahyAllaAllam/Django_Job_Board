from accounts.models import Profile
# import protocol
from accounts.utils import account_activation_token
from blog import views
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from project import settings
# from protocol import protocol
from django.utils.timezone import datetime
from datetime import timedelta
from django.utils import timezone
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, EmailChangeForm
from django.utils.translation import ugettext as _


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Your account has been successfully activated! You are now able to login ') + {user.username} + '!')
        return redirect('login')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.warning(request, _('The activation link is invalid!'))
        return redirect('login')


def register(request):
    emails = User.objects.filter(is_active=True).exclude(email='').values_list('email', flat=True)
    if request.user.is_authenticated:
        messages.success(request, _('You have to logout first!'))
        return redirect('/')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                username = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                for e in emails:
                    if email == e:
                        messages.warning(request, _('Sorry this email already signed up!'))
                        return redirect('accounts:register')
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                link_content = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('accounts:activate', kwargs={
                    'uidb64': link_content['uid'], 'token': link_content['token']})

                activate_url = 'http://' + current_site.domain + link
                email_subject = 'Email Verification'
                c = dict({'username': username, 'activate_url': activate_url})
                text_content = render_to_string('mail_body.txt', c)
                html_content = render_to_string('mail_body.html', c)
                email_message = EmailMultiAlternatives(
                    email_subject,
                    text_content,
                    # '<h1>Hi</h1> ' + user.username + ', \n\n\n' + 'Please click the link below to activate your account \n\n\n' + activate_url,
                    settings.EMAIL_HOST_USER,
                    [email],
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send(fail_silently=False)
                # messages.success(request, f'Your account has been successfully created! You are now able to log in {username} ! ')
                # return redirect('login')
                messages.success(request, _('we have sent you an email to verify your account, please check your mail ! '))

                return redirect('login')
                # return render(request, 'login')
            messages.success(request, _('Please write a valid value!'))
            return redirect('accounts:register')
        else:
            form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form, 'title': _('Register')})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Your account has been updated !'))
            return redirect('accounts:profile_edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': _('Profile')
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def delete_user(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        if request.method == 'POST':
            user.delete()
            messages.success(request, _('Your account has been deleted successfully !'))
            return redirect('logout')
        context = {'title': _('Delete-Account')}
        return render(request, 'accounts/delete_user.html', context)
    else:
        messages.warning(request, _('Oooops you do not have permission to do that!'))
        return redirect('accounts:profile_edit')


def change_email(request):
    if request.method == 'POST':
        e_form = EmailChangeForm(request.POST, instance=request.user)
        if e_form.is_valid():
            e_form.save(commit=False)
            email = e_form.cleaned_data.get('email')
            request.user.is_active = False
            e_form.save()
            current_site = get_current_site(request)
            link_content = {
                'user': request.user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                'token': account_activation_token.make_token(request.user),
            }
            link = reverse('accounts:activate', kwargs={
                'uidb64': link_content['uid'], 'token': link_content['token']})
            activate_url = 'http://' + current_site.domain + link
            email_subject = 'Email Verification'
            c = dict({'username': request.user.username, 'activate_url': activate_url})
            text_content = render_to_string('mail_body.txt', c)
            html_content = render_to_string('mail_body.html', c)
            email_message = EmailMultiAlternatives(
                email_subject,
                text_content,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)
            messages.success(request, _('we have sent you an email to verify your account, please check your mail ! '))
            return redirect('logout')
        messages.success(request, _('Please write a valid email.'))
        return redirect('accounts:change_email')
    e_form = EmailChangeForm(instance=request.user)
    context = {
        'e_form': e_form,
        'title': _('update-Email')
    }
    return render(request, 'accounts/change_email.html', context)


'''
x = request.user.last_login.date()
c = (timezone.now() + 0o7)
print(c)
c = (timezone.now() - datetime.timedelta(days=7))
seven_days_ago = timezone.now() - datetime.timedelta(days=7)
print(seven_days_ago)
value = "f@company.com"

try:
    validate_email(value)
except ValidationError as e:
    print("bad email, details:", e)
else:
    print("good email")


@login_required()
def delete_user(request, username):
    try:
        u = User.objects.get(username=username)
        u.delete()
        messages.success(request, "The user is deleted")

    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return render(request, 'accounts/profile_edit.html')

    except Exception as e:
        return render(request, 'accounts/profile_edit.html', {'err': e.message})

    return render(request, 'accounts/delete_user.html')

'''
