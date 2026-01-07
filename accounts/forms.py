from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]   
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    