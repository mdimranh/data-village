from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django.utils.deprecation import MiddlewareMixin


class AdminMidleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        if path.startswith("/admin") and not path.startswith("/admin/login"):
            if not request.user.is_authenticated:
                return redirect(reverse('login') + f"?redirect={request.path}")
            else:
                if not request.user.is_superuser and not request.user.is_staff:
                    messages.error(request, "You haven't permission to access admin panel.")
                    return redirect('home')