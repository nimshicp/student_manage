from students.models import Student

def generate_unique_roll_no(prefix="STU"):
    last_student = Student.objects.order_by('-id').first()
    if last_student and last_student.roll_no:
        last_number = int(last_student.roll_no.replace(prefix, ""))
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{new_number:04d}"
