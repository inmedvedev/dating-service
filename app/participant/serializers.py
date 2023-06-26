from rest_framework import serializers

from .models import Preference, Rating


class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = (
            'name',
            'attitude',
            'importance',
        )


class PreferenceCreateSerializer(serializers.ModelSerializer):
    participant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Preference
        fields = (
            'participant',
            'name',
            'attitude',
            'importance',
        )


class PreferenceDeleteSerializer(serializers.ModelSerializer):
    participant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Preference
        fields = (
            'participant',
            'name',
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
            'other_participant',
            'rating',
        )
