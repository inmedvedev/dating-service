from django.core.management import BaseCommand
from django.db import transaction
from pathlib import Path
import uuid
import json

from participant.models import Participant, Preference
from account.models import User


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            type=Path,
            required=True,
            help='Filepath to participants.json',
        )

    def handle(self, *args, **options):
        filepath = options['path']
        preferences = []
        participants = []
        users = []
        for participant_info in readline_generator(filepath):
            uid = uuid.uuid4()
            user = User(email=f'{uid}@mail.ru')
            users.append(user)
            participant = Participant(
                id=uid,
                user=user,
                first_name=participant_info['name'].split(' ')[1],
                last_name=participant_info['name'].split(' ')[0],
            )
            participants.append(participant)
            for name, params in participant_info['precedents'].items():
                preferences.append(
                    Preference(
                        participant=participant,
                        name=name,
                        **params,
                    )
                )
        with transaction.atomic():
            User.objects.bulk_create(objs=users)
            Participant.objects.bulk_create(objs=participants)
            Preference.objects.bulk_create(objs=preferences)


def readline_generator(filepath):
    with open(filepath) as file:
        while True:
            participant_info = file.readline()
            if not participant_info:
                break
            yield json.loads(participant_info)
