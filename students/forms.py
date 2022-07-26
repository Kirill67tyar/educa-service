from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from courses.models import Course


class RegistrationModelForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2',)

    def save(self, force_insert=False, force_update=False, commit=True):
        user_instance = super().save(commit=False)
        cd = self.cleaned_data
        user_instance.set_password(cd['password'])
        if commit:
            user_instance.save()
        return user_instance

    def clean_password2(self, *args, **kwargs):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            self.error = forms.ValidationError('Пароли не совпадают')
            raise self.error
        return cd['password2']


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.HiddenInput
    )
