from django import forms


class ConnexionForm(forms.Form):
    username=forms.CharField(max_length=150,widget=forms.TextInput(),required=True)
    password=forms.CharField(min_length=8,widget=forms.PasswordInput(), required=True)

class RegistrationForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(),required=True)
    username=forms.CharField(max_length=150,widget=forms.TextInput(),required=True)
    password1=forms.CharField(min_length=8,widget=forms.PasswordInput(),required=True)
    password2=forms.CharField(min_length=8,widget=forms.PasswordInput(),required=True)