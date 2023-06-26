from django.db import models
from django.conf import settings
import uuid


class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    first_name = models.CharField('Имя', max_length=100, blank=True)
    last_name = models.CharField('Фамилия', max_length=100, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Preference(models.Model):
    ATTITUDE_CHOICES = [
        ('negative', 'Отрицательное'),
        ('positive', 'Положительное'),
    ]
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, blank=True)
    name = models.CharField('Название', max_length=100, blank=True)
    attitude = models.CharField(
        'Отношение', max_length=20, choices=ATTITUDE_CHOICES, blank=True, null=True
    )
    importance = models.PositiveSmallIntegerField('Важность', blank=True, null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, blank=True, related_name='ratings'
    )
    other_participant = models.ForeignKey(
        Participant, on_delete=models.CASCADE, blank=True
    )
    rating = models.SmallIntegerField('Рейтинг', blank=True)

    def __str__(self):
        return f'{self.other_participant} {self.rating}'
