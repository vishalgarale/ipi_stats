from django.db import models


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
    def filter_by_season(cls, data):
        return cls.objects.filter(season=data['season'])


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
