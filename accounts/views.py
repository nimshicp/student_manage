from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import RegisterForm
from django.views.decorators.cache import never_cache



@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            
            try:
                send_mail(
                    subject='Welcome to Student Management System',
                    message=(
                        f"Hi {form.cleaned_data['name']},\n\n"
                        f"Your account has been created successfully.\n\n"
                        f"Login Details:\n"
                        f"Email: {user.email}\n\n"
                        f"You can now log in using your email and password.\n\n"
                        f"Thank you!"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(
                    request,
                    "Account created, but welcome email could not be sent."
                )

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_superuser:
                return redirect('students:student_list')

            if hasattr(user, 'profile') and user.profile.role == 'ADMIN':
                return redirect('students:student_list')

            return redirect('dashboard')

    return render(request, 'login.html', {'form': form})


@never_cache
def logout_view(request):
    logout(request)
    return redirect('home')
