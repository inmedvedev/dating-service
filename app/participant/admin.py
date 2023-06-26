from django.contrib import admin
from .models import Participant, Preference, Rating


class PreferenceInline(admin.TabularInline):
    model = Preference


class RatingInline(admin.TabularInline):
    model = Rating
    fk_name = 'participant'
    raw_id_fields = ('other_participant',)


class ParticipantAdmin(admin.ModelAdmin):
    inlines = [
        PreferenceInline,
        RatingInline,
    ]
    search_fields = ('user__email',)


admin.site.register(Participant, ParticipantAdmin)
