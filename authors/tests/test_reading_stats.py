from django.urls import reverse
from .base_test import TestBase
from rest_framework.views import status


class TestReadStats(TestBase):

    def test_get_read_list_status(self):
        """test getting the list of articles read"""
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))
        self.client.get(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'}
            ),
            content_type='application/json'
        )
        response = self.client.get(
            reverse(
                'reading_stats:list_stats',
            )

        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_empty_read_list(self):

        """test get stats for user with no views"""
        self.create_article()
        self.client.get(self.get_verify_url(self.user_data))

        response = self.client.get(
            reverse(
                'reading_stats:list_stats',
            )
        )
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
