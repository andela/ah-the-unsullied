import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList


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
