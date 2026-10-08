from django.urls import include, path
from rest_framework.routers import DefaultRouter

from wisme.api.views import HealthCheckView, PageViewSet

app_name = 'api'

router = DefaultRouter()
router.register('pages', PageViewSet, basename='page')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health'),
    path('', include(router.urls)),
]
