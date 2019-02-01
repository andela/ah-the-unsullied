import json

from rest_framework.views import status
from django.urls import reverse

# local imports
from .base_test import TestBase


class TagCreation(TestBase):
    """Test if a tag list is created"""

    def test_tag_addition(self):
        """Test tags addition to article"""
        self.verify_user()
        response = self.client.post(
            self.article_url,
            data=json.dumps(self.valid_taglist_data),
            content_type='application/json'
        )
        length_of_taglist = len(response.data['tagList'])
        self.assertEqual(length_of_taglist, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tag_update(self):
        """Test tags update"""
        self.verify_user()
        self.client.post(
            self.article_url,
            data=json.dumps(self.valid_taglist_data),
            content_type='application/json'
        )
        response = self.client.put(
            reverse(
                'articles:detail_article',
                kwargs={'slug': 'another-post'},
            ),
            data=json.dumps(self.valid_taglist_update_data),
            content_type='application/json'
        )
        length_of_taglist = len(response.data['tagList'])
        self.assertEqual(length_of_taglist, 4)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
