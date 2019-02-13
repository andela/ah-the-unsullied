from django.urls import path
from .views import ListReadStatsView

app_name = "reading_stats"


urlpatterns = [
    path('', ListReadStatsView.as_view(), name='list_stats'),
]
