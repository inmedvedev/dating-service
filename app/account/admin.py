from django.contrib import admin

from .models import LoginCodeEmail, User

admin.site.register(LoginCodeEmail)
admin.site.register(User)
