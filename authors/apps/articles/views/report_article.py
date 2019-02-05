from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.apps.articles.models import Article, ReportArticle
from authors.apps.articles.response_messages import (error_messages,
                                                     success_messages)
from authors.apps.articles.serializers import ReportArticleSerializer
from authors.apps.authentication.models import User


class ReportArticleApi(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportArticleSerializer

    def post(self, request, *args, **kwargs):
        try:
            # check if article exists
            article = Article.objects.get(slug=kwargs['slug'])
        except Article.DoesNotExist:
            message = {"message": error_messages['article_404']}
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        # you can not report your own article
        if article.author_id == request.user.id:
            message = {"message": error_messages['report_error']}
            return Response(message, status.HTTP_403_FORBIDDEN)

        # check if user had reported this article earlier
        article_exits = ReportArticle.objects.filter(
            slug=kwargs['slug'], reporter_id=article.author.username).first()
        if article_exits:
            message = {"message": error_messages['already_reported']}
            return Response(message, status.HTTP_401_UNAUTHORIZED)

        time_h = datetime.now()
        time = datetime.strftime(time_h, '%d-%B-%Y %H:%M')
        article_reporting = {
            'slug': kwargs['slug'],
            'author_id': article.author.username,
            'message': request.data.get('message'),
            'reporter_id': request.user.username,
        }

        serializer = self.serializer_class(data=article_reporting)
        serializer.is_valid(raise_exception=True)
        hosting = request.get_host()
        username = request.user.username
        author_email = User.objects.filter(
            username=article.author.username).first().email
        email = 'kelvinwmblogs@gmail.com'
        link = 'https://' + hosting + '/api/articles/' + kwargs['slug']
        email_subject = 'Article: ' + kwargs['slug'] + ' has been reported.'
        dev_message = render_to_string(
            'report_article.html', {
                'time': time,
                'slug': kwargs['slug'],
                'username': username,
                'link': link,
                'message': request.data.get('message')
            })
        author_message = render_to_string(
            'user_reported_article.html', {
                'time': time,
                'slug': kwargs['slug'],
                'username': username,
                'link': link,
                'message': request.data.get('message')
            })
        article.is_reported = True
        article.save(update_fields=['is_reported'])

        send_mail(email_subject,
                  'Article: ' + kwargs['slug'] +
                  ' reported.', '', [email, ],
                  html_message=dev_message,
                  fail_silently=False)

        send_mail(email_subject,
                  'Article: ' + kwargs['slug'] +
                  ' reported.', '', [author_email, ],
                  html_message=author_message,
                  fail_silently=False)
        serializer.save()

        message = {"message": success_messages['report_email']}
        return Response(message, status.HTTP_201_CREATED)


class GetReportedArticles(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportArticleSerializer

    def get(self, request):
        article = ReportArticle.objects.filter(
            reporter_id=request.user.username)
        serializer = ReportArticleSerializer(article, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
