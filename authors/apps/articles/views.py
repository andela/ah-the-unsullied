
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# local imports
from .models import Article
from .serializers import ArticleSerializer
from .renderers import ArticleJSONRenderer

# Create your views here.


class CreateArticleView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ArticleSerializer
    renderer_classes = (ArticleJSONRenderer,)
    queryset = Article.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
