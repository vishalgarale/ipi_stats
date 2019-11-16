import pandas as pd
from django.core.management.base import BaseCommand
from season_stats.models import Match, Delivery


class Command(BaseCommand):
    help = 'Load the files into database'

    def handle(self, *args, **kwargs):
        matches_data = pd.read_csv("data/matches.csv").to_dict('records')
        match_generator = (Match(**m) for m in matches_data)
        Match.objects.bulk_create(match_generator)

        deliveries_data = pd.read_csv("data/deliveries.csv").to_dict('records')
        deliveries_generator = (Delivery(**m) for m in deliveries_data)
        Delivery.objects.bulk_create(deliveries_generator)

        # 1st
        # Match.objects.filter(season="2017").values('winner').annotate(winner_count=Count('winner')).order_by('-winner_count')[:4]
        # 2nd
        # Match.objects.filter(season="2017").values('toss_winner').annotate(toss_winner_count=Count('toss_winner')).order_by('-toss_winner_count')[:1]
        # 3rd
        # Match.objects.filter(season="2017").values('player_of_match').annotate(player_of_match_count=Count('player_of_match')).order_by('-player_of_match_count')[:1]
        # 4th
        # Match.objects.filter(season="2017").values('winner').annotate(winner_count=Count('winner')).order_by('-winner_count')[:1]
        # 5th
        # Match.objects.filter(winner="Mumbai Indians").values('venue').annotate(venue_count=Count('venue')).order_by('-venue_count')[0]
        # 6th
        # Match.objects.all().values('toss_decision').annotate(toss_counts=Count('toss_decision'))
        # 7th
        # 8th
        # Match.objects.all().order_by('-win_by_runs')[0]
        # 9th
        # Match.objects.all().order_by('-win_by_wickets')[0]
        # 10th
        # Match.objects.filter(winner= F('toss_winner') ).count()
        # 11th
        # Delivery.objects.filter(match_id__in=Match.objects.filter(season='2008')).values('batsman', 'match_id').annotate(match_run=Sum('batsman_runs')).order_by('-match_run')[0]
        # 12th
        # Delivery.objects.filter(match_id__in=Match.objects.filter(season='2008')).values('batsman', 'match_id').annotate(match_run=Sum('batsman_runs')).order_by('-match_run')[0]
        # 13th
        # Delivery.objects.filter(dismissal_kind="caught").values('match_id', 'fielder').annotate(catch_counts=Count('fielder')).order_by('-catch_counts')[0]
