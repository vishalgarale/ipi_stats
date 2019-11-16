from rest_framework import routers
from .views import StatsViewSet

router = routers.SimpleRouter()
router.register(r'stats', StatsViewSet)

urlpatterns = router.urls
