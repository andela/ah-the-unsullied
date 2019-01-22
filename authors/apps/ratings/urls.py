from django.urls import path
from .views import RateArticleView

app_name = 'ratings'

article_rating = RateArticleView.as_view({
    'post': 'create',
})

urlpatterns = [
    path('articles/<slug>/rate-article', article_rating,
         name='article_rating'),
]
