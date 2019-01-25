from django.urls import path
from .views import ArticleRatingAPIView

app_name = 'ratings'

article_rating = ArticleRatingAPIView.as_view()

urlpatterns = [
    path('articles/<slug>/rate-article', article_rating,
         name='article_rating'),
]
