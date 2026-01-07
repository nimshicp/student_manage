from django import forms
from .models import Student
from courses.models import Course
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.core.validators import validate_email

class StudentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Student
        fields = [
            'name',
            'email',
            'date_of_birth',
            'image',
            'courses',
            'year_of_admission',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):

        email = self.cleaned_data.get('email')
        if email:
            try:
             
               validate_email(email)
            except ValidationError:
                raise ValidationError("Please enter a valid email address containing '@'.")
        
            student_instance = self.instance
            user_query = User.objects.filter(email__iexact=email)
            if student_instance and student_instance.user:
                user_query = user_query.exclude(pk=student_instance.user.pk)

            if user_query.exists():
                raise ValidationError("This email is already associated with another user.")
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        
        if len(name) < 3:
            raise ValidationError("Name must be at least 3 characters long.")

        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationError("Name should only contain letters and spaces.")

        return name
    
