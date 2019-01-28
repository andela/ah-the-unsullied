from django.urls import path

from authors.apps.articles.views.comments import(
    CommentsListView,
    CommentsRetrieveUpdateDestroy
)
from authors.apps.articles.views.articles import (GetUpdateDeleteArticle,
                                                  CreateArticleView)

"""
Django 2.0 requires the app_name variable set when using include namespace
"""
app_name = 'articles'

urlpatterns = [

    path('', CreateArticleView.as_view(),
         name='article_create'),
    path('/<slug:slug>', GetUpdateDeleteArticle.as_view(),
         name='detail_article'),
    path('/<slug>/comments', CommentsListView.as_view(), name='comment'),
    path('/<slug>/comments/<int:id>',
         CommentsRetrieveUpdateDestroy.as_view(), name='thread'
         )
]
