from celery import shared_task

from .models import Preference, Participant, Rating


@shared_task
def make_rating(user_id, participant_id):
    user_preferences = Preference.objects.filter(participant__id=participant_id)

    preferences_name = [preference.name for preference in user_preferences]
    participants = (
        Participant.objects.exclude(user__id=user_id)
        .filter(preference__name__in=preferences_name)
        .distinct()
        .prefetch_related('preference_set')
    )
    participants_with_rating = []
    compatibility_count = 0
    for participant in participants:
        if compatibility_count >= 10:
            break
        common_sum_numerator = 0
        common_sum_denominator = 0
        for preference in user_preferences:
            same_preference_queryset = participant.preference_set.filter(
                name=preference.name
            )
            if not same_preference_queryset:
                continue
            same_preference = same_preference_queryset.get()
            multiplier = -1 if preference.attitude != same_preference.attitude else 1
            common_sum_numerator += (
                preference.importance + same_preference.importance
            ) * multiplier
            common_sum_denominator += preference.importance + same_preference.importance
        if common_sum_denominator == 0:
            participant.rating = 0
        else:
            participant.rating = int(
                common_sum_numerator / common_sum_denominator * 100
            )
        if participant.rating >= 75:
            compatibility_count += 1
            participants_with_rating.append(participant)
    participants_with_rating.sort(
        key=lambda participant: participant.rating,
        reverse=True,
    )
    participant_obj = Participant.objects.filter(user__id=user_id).get()
    ratings = []
    for participant in participants_with_rating:
        ratings.append(
            Rating(
                participant=participant_obj,
                other_participant=participant,
                rating=participant.rating,
            )
        )
    Rating.objects.bulk_create(objs=ratings)
