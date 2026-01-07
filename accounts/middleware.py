from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth import get_user_model



class PreventBackToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return response


User = get_user_model()

class ForceLogoutDeletedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                User.objects.get(pk=request.user.pk)
            except User.DoesNotExist:
                logout(request)
                return redirect('login')

        response = self.get_response(request)
        return response