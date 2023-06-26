from django.db import models
from django.conf import settings


class LoginCodeEmail(models.Model):
    email = models.EmailField('Email', blank=True, null=True)
    code = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Код авторизации для email'
        verbose_name_plural = 'Коды авторизации для email'

    def __str__(self):
        if self.email:
            return f"{self.email} {self.timestamp}"
