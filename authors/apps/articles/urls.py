from django.urls import path

from authors.apps.articles.models import LikeDislike
from authors.apps.articles.views.articles import (GetUpdateDeleteArticle,
                                                  CreateArticleView,
                                                  LikeDislikeArticleView)
from authors.apps.articles.views.bookmark import (BookmarkArticle,
                                                  GetBookmarkedArticles)
from authors.apps.articles.views.comments import (
    CommentsListView, CommentsRetrieveUpdateDestroy, CommentHistoryListView,
    LikeDislikeCommentsView
)
from authors.apps.articles.views.favorite import (FavouriteArticle,
                                                  GetFavouriteArticles)
from authors.apps.articles.views.articles import (
     GetUpdateDeleteArticle,CreateArticleView,
     SearchFilter,LikeDislikeArticleView,
     ShareArticleViaEmail,ShareArticleViaFacebook,
     ShareArticleViaTwitter
     )

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
         ),
    path('/<slug>/like',
         LikeDislikeArticleView.as_view(vote_type=LikeDislike.LIKE),
         name='article-like-like'),
    path('/<slug>/dislike',
         LikeDislikeArticleView.as_view(vote_type=LikeDislike.DISLIKE),
         name='article-like-dislike'),
    path('/<slug>/favorite', FavouriteArticle.as_view(),
         name='favorite_article'),
    path('/favorite/', GetFavouriteArticles.as_view(),
         name='all_favourite_article'),
    path('/<slug>/bookmark', BookmarkArticle.as_view(),
         name='bookmark_article'),
    path('/bookmark/', GetBookmarkedArticles.as_view(),
         name='bookmarked_articles'),
    path('/<slug>/comments/<comment_id>/history',
         CommentHistoryListView.as_view(),
         name='comment-history'),
    path('/<slug>/comments/<int:comment_id>/like',
         LikeDislikeCommentsView.as_view(vote_type=LikeDislike.LIKE),
         name='like-comment'
         ),
    path('/<slug>/comments/<int:comment_id>/dislike',
         LikeDislikeCommentsView.as_view(vote_type=LikeDislike.DISLIKE),
         name='dislike-comment'),
    path('/<slug>/email/share',
         ShareArticleViaEmail.as_view(), name='email_share'
         ),
    path('/<slug>/facebook/share',
         ShareArticleViaFacebook.as_view(), name='facebook_share'
         ),
    path('/<slug>/twitter/share',
         ShareArticleViaTwitter.as_view(), name='twitter_share'
         )
]
