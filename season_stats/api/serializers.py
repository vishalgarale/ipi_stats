from rest_framework import serializers
from season_stats.models import Match, Delivery


class MatchSerializer(serializers.ModelSerializer):
    winner_count = serializers.ReadOnlyField()
    toss_winner_count = serializers.ReadOnlyField()
    player_of_match_count = serializers.ReadOnlyField()
    venue_count = serializers.ReadOnlyField()
    win_by_runs = serializers.ReadOnlyField()
    win_by_wickets = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()

    class Meta:
        model = Match
        fields = ['winner', 'winner_count', 'toss_winner', 'toss_winner_count', 'player_of_match', 'player_of_match_count', 'venue', 'venue_count',  'season',	'city',	 'team1', 'team2', 'win_by_runs', 'win_by_wickets', 'date']


class DeliverySerializer(serializers.ModelSerializer):
    match_run = serializers.ReadOnlyField()
    catch_counts = serializers.ReadOnlyField()

    class Meta:
        model = Delivery
        fields = ['batsman', 'match_run', 'match_id', 'catch_counts', 'fielder']