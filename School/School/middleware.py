# middleware.py
from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve
import re


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        current_path = request.path_info.lstrip('/')
        if not any(url.match(current_path) for url in self.exempt_urls):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL)

        response = self.get_response(request)
        return response
