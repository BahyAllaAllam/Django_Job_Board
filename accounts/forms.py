# from accounts.models import Profile
from accounts.models import Profile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=150, help_text=_('Required. 150 characters or fewer.'))

    class Meta:
        model = User
        fields = [_('username'), _('email'), _('password1'), _('password2')]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [_('username'), _('first_name'), _('last_name')]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [_('image')]


class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, help_text=_('Required. 150 characters or fewer.'))

    class Meta:
        model = User
        fields = {_('email')}
