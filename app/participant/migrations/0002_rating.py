# Generated by Django 4.2 on 2023-06-25 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('participant', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.SmallIntegerField(blank=True, verbose_name='Рейтинг')),
                ('other_participant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='participant.participant')),
                ('participant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='participant.participant')),
            ],
        ),
    ]
