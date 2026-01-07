from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(label="Registered Email")
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(
                "You are not authorized to register. Please contact admin."
            )

        if user.has_usable_password():
            raise forms.ValidationError(
                "This account is already registered. Please login."
            )

        return email

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])  
        user.save()
        return user
