from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .models import LoginCodeEmail


class LoginCodeEmailBackend(ModelBackend):
    """Бэкенд для аутентификации посредством кодов авторизации в email"""

    def authenticate(self, request, email=None, email_code=None, **kwargs):
        if not email or not email_code:
            return

        try:
            user = get_user_model().objects.get(email=email)

            if not self.user_can_authenticate(user):
                return
            login_code = LoginCodeEmail.objects.filter(email=user, code=email_code)
            if not login_code.exists():
                return
            return user

        except (get_user_model().DoesNotExist, LoginCodeEmail.DoesNotExist):
            return
