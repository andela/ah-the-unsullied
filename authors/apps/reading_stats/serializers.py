from rest_framework import serializers

from .models import ReadingStats


class ReadStatsSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, reading_stat):
        user = reading_stat.user.username
        return user

    def get_article(self, stats_object):
        return {
            "article": stats_object.article.title,
            "slug": stats_object.article.slug
        }

    class Meta:
        model = ReadingStats
        fields = ['article', 'user']
