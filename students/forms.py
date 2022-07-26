from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


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

    def clean_password2(self, *args, **kwargs):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        cd['password'] = cd['password2'] = make_password(cd['password'])
        return cd['password2']
