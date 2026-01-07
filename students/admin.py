from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "roll_no", "year_of_admission")
    search_fields = ("roll_no", "user__username")
