import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList
import operator
from functools import reduce


class ArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        try:
            articles = len(data['results'])
            if articles > 0:
                return json.dumps({
                    'articles': data,
                    'articles_count': articles
                })
        except:
            return json.dumps({
                'article': data,
            })


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, ReturnList):
            return json.dumps({
                'comments': data,
                'comments_count': len(data)
            })
        return json.dumps({
            'comment': data
        })


class LikeArticleJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({
            'likes_dislikes_count': data
        })


class TagJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        tags = len(data)
        if tags > 0:
            return json.dumps({
                'tags': reduce(operator.concat, [list(i.values()) for i in
                                                 data['results']])
            })
        return json.dumps({
            'tag': list(data['results'][0].values()),
        })
