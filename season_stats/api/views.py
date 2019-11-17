from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Exists, OuterRef, Subquery
from .serializers import MatchSerializer, DeliverySerializer
from season_stats.models import Match, Delivery


class StatsViewSet(viewsets.ViewSet):
    queryset = Match.objects.all()
    
    @action(detail=False, methods=['post'])
    def most_wins(self, request):
        __doc__ = "Top 4 teams in terms of wins & Which team won max matches in the whole season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        limit = int(request.data.get('limit', 1))

        queryset = Match.get_most_wins(season=request.data.get('season'), limit=limit)

        serializer_data = MatchSerializer(queryset, many=True)

        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_tosses_wins(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        limit = int(request.data.get('limit', 1))

        queryset = Match.get_most_tosses_wins(season=request.data.get('season'), limit=limit)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_mom_wins(self, request):
        __doc__ = "Which player won the maximum number of Player of the Match awards in the whole season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Match.get_most_mom_wins(season=request.data.get('season'), limit=limit)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_location_wins_for_top_team(self, request):
        __doc__ = "Which location has the most number of wins for the top team"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Match.get_most_location_wins_for_top_team(season=request.data.get('season'), limit=1)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def bat_first_per(self, request):
        __doc__ = "Which location has the most number of wins for the top team"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        queryset = Match.get_toss_decisions(season=request.data.get('season'))

        batting_win_count = 0
        total_count = 0
        for d in queryset:
            if d['toss_decision'] == 'bat':
                batting_win_count = d['toss_counts']
            total_count += d['toss_counts']

        bat_first_win_per = batting_win_count / total_count * 100

        return Response({ "bat_first_win_percentage": bat_first_win_per }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_matches_hosted_location(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Match.get_most_matches_hosted_location(season=request.data.get('season'), limit=limit)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def highest_margin_win_by_runs(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Match.get_highest_margin_win_by_runs(season=request.data.get('season'), limit=limit)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def highest_margin_win_by_wickets(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Match.get_highest_margin_win_by_wickets(season=request.data.get('season'), limit=limit)
        serializer_data = MatchSerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def team_won_toss_and_match_count(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Match.objects.filter(winner= F('toss_winner') ).count()
        return Response( {"team_won_toss_and_match_count": queryset}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_runs_in_match(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Delivery.get_most_runs_in_match(season=request.data.get('season'), limit=limit)
        serializer_data = DeliverySerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def most_catches_in_match(self, request):
        __doc__ = "Which team won the most number of tosses in the season"

        if not request.data.get('season', None):
            return Response({"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)

        limit = int(request.data.get('limit', 1))

        queryset = Delivery.get_most_catches_in_match(season=request.data.get('season'), limit=limit)
        serializer_data = DeliverySerializer(queryset, many=True)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
