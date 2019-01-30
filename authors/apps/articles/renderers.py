import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList
import json


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            return json.dumps({
                'articles': data,
                'ArticleCount': len(data)
            })
        return json.dumps({
            'article': data
        })


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            return json.dumps({
                'comments': data,
                'commentsCount': len(data)
            })
        return json.dumps({
            'comment': data
        })


class LikeArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'likes_dislikes': data
        })
