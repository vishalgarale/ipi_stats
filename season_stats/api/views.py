from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When, Exists, OuterRef, Subquery
from .serializers import MatchSerializer
from season_stats.models import Match, Delivery


class StatsViewSet(viewsets.ViewSet):
    queryset = Match.objects.all()
    
    @action(detail=False, methods=['post'])
    def top_team_wins(self, request):
        
        if not request.data.get('season', None):
            return Response( {"message": "Season is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        limit = int(request.data.get('limit', 1))

        queryset = Match.filter_by_season(request.data) \
                        .values('winner') \
                        .annotate(winner_count=Count('winner')) \
                        .order_by('-winner_count')[:limit]

        serializer_data = MatchSerializer(queryset, many=True)

        return Response(serializer_data.data, status=status.HTTP_200_OK)