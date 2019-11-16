from rest_framework import serializers
from season_stats.models import Match, Delivery


class MatchSerializer(serializers.ModelSerializer):
    winner_count = serializers.ReadOnlyField()

    class Meta:
        model = Match
        fields = ['winner', 'winner_count']