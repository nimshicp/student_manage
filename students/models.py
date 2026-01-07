
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class Student(models.Model):
    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="student",
    null=True,
    blank=True
    )

    roll_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='students', blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    courses = models.ManyToManyField(Course, blank=True, related_name='students' )
    year_of_admission = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

    


