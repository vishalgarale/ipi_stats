from django.db import models
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Exists, OuterRef, Subquery


class Match(models.Model):
    TOSS_CHOICES = (
        ('bat', 'bat'),
        ('field', 'field'),
    )

    RESULT_CHOICES = (
        ('no result', 'no result'),
        ('normal', 'normal'),
        ('tie', 'tie')
    )

    season = models.CharField(max_length=50, default="", blank=False)
    city = models.CharField(max_length=50, default="", blank=False)
    date = models.DateField(blank=False)
    team1 = models.CharField(max_length=50, default="", blank=False)
    team2 = models.CharField(max_length=50, default="", blank=False)
    toss_winner = models.CharField(max_length=50, default="", blank=False)
    toss_decision = models.CharField(max_length=50, choices=TOSS_CHOICES)
    result = models.CharField(max_length=50, choices=RESULT_CHOICES)
    dl_applied = models.BooleanField()
    winner = models.CharField(max_length=50, default="", blank=False)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=50, default="", blank=False)
    venue = models.CharField(max_length=250, default="", blank=False)
    umpire1 = models.CharField(max_length=50, default="", blank=False)
    umpire2 = models.CharField(max_length=50, default="", blank=False)
    umpire3 = models.CharField(max_length=50, default="", blank=False)

    class Meta:
        db_table = 'matches'

    @classmethod
    def filter_by_season(cls, season):
        return cls.objects.filter(season=season)

    @classmethod
    def get_most_wins(cls, season, limit):
        return cls.filter_by_season(season) \
                  .values('winner') \
                  .annotate(winner_count=Count('winner')) \
                  .order_by('-winner_count')[:limit]

    @classmethod
    def get_most_tosses_wins(cls, season, limit):
        return cls.filter_by_season(season) \
                  .values('toss_winner') \
                  .annotate(toss_winner_count=Count('toss_winner')) \
                  .order_by('-toss_winner_count')[:limit]

    @classmethod
    def get_most_mom_wins(cls, season, limit):
        return cls.filter_by_season(season) \
                  .values('player_of_match') \
                  .annotate(player_of_match_count=Count('player_of_match')) \
                  .order_by('-player_of_match_count')[:limit]

    @classmethod
    def get_most_location_wins_for_top_team(cls, season, limit):
        most_wins_team = Match.get_most_wins(season=season, limit=1)
        return cls.objects.filter(winner=most_wins_team[0]['winner']) \
                          .values('venue') \
                          .annotate(venue_count=Count('venue')) \
                          .order_by('-venue_count')[:limit]

    @classmethod
    def get_toss_decisions(cls, season):
        return cls.objects.all() \
                  .values('toss_decision') \
                  .annotate(toss_counts=Count('toss_decision'))

    @classmethod
    def get_most_matches_hosted_location(cls, season, limit):
        return cls.filter_by_season(season) \
                  .values('venue') \
                  .annotate(venue_count=Count('venue')) \
                  .order_by('-venue_count')[:limit]

    @classmethod
    def get_highest_margin_win_by_runs(cls, season, limit):
        return cls.filter_by_season(season).order_by('-win_by_runs')[:limit]

    @classmethod
    def get_highest_margin_win_by_wickets(cls, season, limit):
        return cls.filter_by_season(season).order_by('-win_by_wickets')[:limit]


class Delivery(models.Model):

    INNING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4)
    )

    match = models.ForeignKey(Match, related_name='deliveries', on_delete=models.CASCADE)
    inning = models.SmallIntegerField(choices=INNING_CHOICES)
    batting_team = models.CharField(max_length=50, default="", blank=False)
    bowling_team = models.CharField(max_length=50, default="", blank=False)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=50, default="", blank=False)
    non_striker = models.CharField(max_length=50, default="", blank=False)
    bowler = models.CharField(max_length=50, default="", blank=False)
    is_super_over = models.BooleanField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=50, default="", blank=False)
    dismissal_kind = models.CharField(max_length=50, default="", blank=False)
    fielder = models.CharField(max_length=50, default="", blank=False)

    class Meta:
        db_table = 'deliveries'

    @classmethod
    def get_most_runs_in_match(cls, season, limit):
        all_season_match_ids = Match.filter_by_season(season=season).values_list('id', flat=True)
        return cls.objects.filter(match_id__in=all_season_match_ids) \
                  .values('batsman', 'match_id') \
                  .annotate(match_run=Sum('batsman_runs')) \
                  .order_by('-match_run')[:limit]

    @classmethod
    def get_most_catches_in_match(cls, season, limit):
        all_season_match_ids = Match.filter_by_season(season=season).values_list('id', flat=True)
        return cls.objects.filter(match_id__in=all_season_match_ids, dismissal_kind="caught") \
                  .values('fielder', 'match_id') \
                  .annotate(catch_counts=Count('fielder')) \
                  .order_by('-catch_counts')[:limit]