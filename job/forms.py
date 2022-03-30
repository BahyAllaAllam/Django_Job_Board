from django import forms
from .models import Job_applicant, Job
from django.utils.translation import gettext as _


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Job_applicant
        fields = [_('name'), _('email'), _('portfolio_link'), _('cv'), _('cover_letter')]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': _('Your name')})
        self.fields['email'].widget.attrs.update({'placeholder': _('Email')})
        self.fields['portfolio_link'].widget.attrs.update({'placeholder': _('Website/Portfolio link')})
        self.fields['cv'].widget.attrs.update(
            {'class': 'custom-file-input', 'id': 'inputGroupFile03', 'aria-describedby': 'inputGroupFileAddon03'})
        self.fields['cover_letter'].widget.attrs.update({'placeholder': _('Coverletter')})


class JobForm(forms.ModelForm):
    publish = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('owner', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['job_type'].widget.attrs.update({'id': 'job_type'})
        self.fields['requirements'].widget.attrs.update(
            {'placeholder': _('Please start the sentence in a new line and put a full stop after each sentence.')}
        )
