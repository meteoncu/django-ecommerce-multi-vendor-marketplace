from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.http import HttpResponseRedirect
from django.urls import get_script_prefix, is_valid_path
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.utils import timezone
from user.models import AuthToken


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.headers.get("Authorization", None)

        if token:
            print(token)
            auth_token = AuthToken.objects.filter(token=token).first()

            if auth_token and auth_token.expire_date > timezone.now():
                request.__setattr__("user", auth_token.user)
