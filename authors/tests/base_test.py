# django imports
import json
import os
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.test import APITestCase, APIClient

# local imports
from authors.apps.authentication.activate import account_activation_token
from authors.apps.authentication.models import User


class TestBase(APITestCase):
    """This class defines the basic setup for the tests
        and the dummy data used for the tests.
    """

    def setUp(self):
        """This method is used to initialize variables used by the tests."""

        self.client = APIClient()
        self.unauthenticated_client = APIClient()
        self.login_url = reverse('authentication:login_url')
        self.user_url = reverse('authentication:signup_url')
        self.update_url = reverse('authentication:user_update')
        self.article_url = reverse('articles:article_create')
        self.social_auth_url = reverse('authentication:social_auth')
        self.base_url = os.getenv('BASE_URL')

        self.user_data = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}
        self.rater_data = {
            "user": {
                "username": "allan",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}
        self.update_data = {
            "user": {
                "username": "sam2",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@2"
            }}
        self.test_username = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_username2 = {
            "user": {
                "username": "sam",
                "email": "sly@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.empty_email = {
            "user": {
                "username": "sam",
                "email": "",
                "password": "A23DVFRss@"
            }}

        self.blank_mail = {
            "email": ""
        }

        self.empty_password = {
            "user": {
                "username": "sam",
                "email": "sami@gmail.com",
                "password": ""
            }}

        self.empty_username = {
            "user": {
                "username": "",
                "email": "sami@gmail.com",
                "password": "904438283278"
            }}

        self.login_data = {
            "user": {
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_wrong_login = {
            "user": {
                "email": "sammy@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.test_empty_email = {
            "user": {
                "email": "",
                "password": "A23@"
            }}

        self.test_login_unregistered = {
            "user": {
                "email": "sammy@gmail.com",
                "password": "A23@"
            }}
        self.signup_user_data = {
            'user': {
                'username': 'Allan123',
                'email': 'cake@foo.com',
                'password': 'Yertg234D#'
            }
        }
        self.reset_password_email = {
            "email": "sam@gmail.com"
        }
        self.inexistent_email = {
            "email": "job@yahoo.com"
        }
        self.reset_password_invalid_email = {
            "email": "kenyamoja@gmail.com"
        }
        self.new_article = {
            'title': 'test',
            'description': 'learn TDD',
            'body': 'best tests are done at night'
        }
        self.comment_data = {
            'body': 'poseidon'
        }

        self.edit_data = {
            "comment": {
                'body': 'sammy'
            }}

        self.update_comment_data = {
            'body': 'poseidon'
        }

        self.thread_data = {
            "comment": {
                'body': 'poseidon'}
        }

        self.update_child_data = {
            "comment": {
                'body': 'theus'}
        }

        self.valid_article_data = {
            "article": {
                "title": "another post",
                "description": "a fitting description",
                "body": "a body field",
                "tag_list": []
            }
        }

        self.valid_taglist_data = {
            "article": {
                "title": "another post",
                "description": "a fitting description",
                "body": "a body field",
                "tag_list": ["tag1", "tag2"]
            }
        }

        self.valid_taglist_update_data = {
            "article": {
                "title": "another post",
                "description": "a fitting description",
                "body": "a body field",
                "tag_list": ["tag1", "tag2", "tag3", "tag4"]
            }
        }

        self.invalid_article_data = {
            "article": {
                "title": "another post",
                "description": "a fitting description"
            }
        }

        self.null_article_data = {
            "article": {

            }
        }

        self.different_user_data = {
            "user": {
                "username": "nesh",
                "email": "nesh@gmail.com",
                "password": "A23DVFRss@"
            }}

        self.user_data2 = {
            "user": {
                "username": "abdi",
                "email": "abdi@gmail.com",
                "password": "A23DVFRss@"
            }
        }

        self.invalid_token = {
            "provider": "google-oauth2",
            "access_token": "tjdjdj"
        }

        self.invalid_provider = {
            "provider": "guth2",
            "access_token": "tjdjdj",
        }

        self.no_backend = {
        }

        self.new_article = {
            'title': 'test',
            'description': 'learn TDD',

            'body': 'best tests are done at night'
        }

        self.user_data = {
            "user": {
                "username": "sam",
                "email": "sam@gmail.com",
                "password": "A23DVFRss@"
            }
        }

        self.user_data3 = {
            "user": {
                "username": "job",
                "email": "job@gmail.com",
                "password": "A23DVFRss@"
            }
        }
        self.update_data = {
            "user": {
                "bio": "catherine"
            }
        }

        self.rating = {
            "rating": "3"
        }

        self.another_rating = {
            "rating": "4"
        }

        self.wrong_rating = {
            "rating": "9"
        }

        self.non_user_token = 'Bearer Token'

        self.share_email_data = {
            "email": "jake@gmail.com"
        }

        self.highlight_index = {
            "comment": {
                "body": "you should uncomment this",
                "begin_index": "1",
                "end_index": "15"
            }
        }
        self.update_highlight_index = {
            "comment": {
                "body": "This is an update",
                "begin_index": "1",
                "end_index": "15"
            }
        }
        self.highlight_larger_start_index = {
            "comment": {
                "body": "you should uncomment this",
                "begin_index": "15",
                "end_index": "1"
            }
        }
        self.highlight_non_integer_index = {
            "comment": {
                "body": "you should uncomment this",
                "begin_index": "a",
                "end_index": "b"
            }
        }

    def get_token_on_signup(self, ):
        return self.client.post(
            reverse('authentication:signup_url'),
            data=json.dumps(self.user_data),
            content_type='application/json'
        )

    def authentication_token(self, ):
        res = self.get_token_on_signup()
        token = res.data['token']
        return token
        self.share_email_data = {
            "email": "jake@gmail.com"
        }

    def get_token(self):
        """Register and login a user"""

        self.client.post(
            self.user_url,
            self.user_data,
            format='json'
        )
        self.client.get(self.get_verify_url(self.user_data))
        response = self.client.post(
            self.login_url,
            self.login_data,
            format="json"
        )
        token = response.data['token']
        return token

    def get_verify_url(self, user):
        self.register_user()
        user_to_activate = User.objects.get(username=user['user']['username'])
        pk = urlsafe_base64_encode(force_bytes(user_to_activate.id)).decode()
        token = account_activation_token.make_token(user_to_activate)
        url = reverse('authentication:activate', kwargs={"pk": pk,
                                                         "token": token})
        return url

    def register_user(self):
        return self.client.post(
            self.user_url,
            self.user_data,
            format='json'
        )

    def register_duplicate_email(self, ):
        return self.client.post(
            self.user_url,
            self.user_data,
            format='json'
        )

    def register_duplicate_username(self, ):
        return self.client.post(
            self.user_url,
            self.test_username2,
            format='json'
        )

    def register_empty_email(self, ):
        return self.client.post(
            self.user_url,
            self.empty_email,
            format='json'
        )

    def register_empty_password(self, ):
        return self.client.post(
            self.user_url,
            self.empty_password,
            format='json'
        )

    def register_empty_username(self, ):
        return self.client.post(
            self.user_url,
            self.empty_username,
            format='json'
        )

    def login_user(self):
        return self.client.post(
            self.login_url,
            self.login_data,
            format="json"
        )

    def login_wrong_user_details(self, ):
        return self.client.post(
            self.login_url,
            self.test_wrong_login,
            format="json"
        )

    def dynamic_register_user(self, data):
        return self.client.post(
            self.user_url,
            data,
            format='json'
        )

    def login_empty_email(self, ):
        return self.client.post(
            self.login_url,
            self.test_empty_email,
            format="json"
        )

    def get_comment_url(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        return url

    def get_child_comment_url(self):
        slug = self.create_article().data['slug']
        comment_url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(
            comment_url, self.comment_data, format="json")
        id = response.data['id']
        url = reverse("articles:thread", kwargs={"slug": slug, "id": id})
        return url

    def get_nonexistant_child_comment_url(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:thread", kwargs={"slug": slug, "id": 3})
        return url

    def comment_on_nonexistant_comment(self):
        comment_url = self.get_nonexistant_child_comment_url()
        response = self.client.post(
            comment_url, self.comment_data, format="json")
        return response

    def create_article(self, ):
        token = self.authentication_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))
        return self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )

    def get_token_signup_different_user(self):
        return self.client.post(
            reverse('authentication:signup_url'),
            data=json.dumps(self.user_data2),
            content_type='application/json'
        )

    def get_token_signup_user_3(self):
        return self.client.post(
            reverse('authentication:signup_url'),
            data=json.dumps(self.user_data3),
            content_type='application/json'
        )

    def authentication_token_2(self, ):
        res = self.get_token_signup_different_user()
        token = res.data['token']
        return token

    def follow(self):
        token = self.authentication_token()
        url = reverse('profiles:profile_details',
                      kwargs={'username': 'sam'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(url)
        self.authentication_token_2()
        follow_url = reverse('profiles:follow',
                             kwargs={'username': 'abdi'})
        return self.client.post(follow_url)

    def verify_user(self):
        token = self.authentication_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))

    def authentication_token_3(self, ):
        res = self.get_token_signup_user_3()
        token = res.data['token']
        return token

    def edit_comment(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:comment", kwargs={"slug": slug})
        response = self.client.post(url, self.comment_data, format="json")
        comment_id = response.data['id']
        edit_url = reverse(
            "articles:thread",
            kwargs={"slug": slug, "id": comment_id})
        self.client.put(edit_url, self.edit_data, format="json")
        return [slug, comment_id]

    def edit_history_url(self, slug, id):
        return reverse(
            "articles:comment-history",
            kwargs={"slug": slug, "comment_id": id})

    def share_article_via_email(self):
        slug = self.create_article().data['slug']
        email_share_url = reverse(
            "articles:email_share", kwargs={"slug": slug})
        return self.client.post(
            email_share_url, self.share_email_data, format="json")

    def share_article_via_facebook(self):
        slug = self.create_article().data['slug']
        facebook_share_url = reverse(
            "articles:facebook_share", kwargs={"slug": slug})
        return facebook_share_url

    def share_article_via_twitter(self):
        slug = self.create_article().data['slug']
        twitter_share_url = reverse(
            "articles:twitter_share", kwargs={"slug": slug})
        return twitter_share_url

    def single_highlight_comment_url(self):
        slug = self.create_article().data['slug']
        highlighting_url = reverse("articles:highlight", kwargs={"slug": slug})
        response = self.client.post(
            highlighting_url, self.highlight_index, format="json")
        id = response.data['id']
        url = reverse("articles:highlight_comment",
                      kwargs={"slug": slug, "id": id})
        return url

    def single_nonexistant_highlight_comment_url(self):
        slug = self.create_article().data['slug']
        url = reverse("articles:highlight", kwargs={"slug": slug})
        self.client.post(url, self.highlight_index, format="json")
        url = reverse("articles:highlight_comment",
                      kwargs={"slug": slug, "id": 18})
        return url

    def single_highlight_comment_non_existant_article_url(self):
        self.verify_user()
        url = reverse("articles:highlight", kwargs={"slug": "slug"})
        self.client.post(url, self.highlight_index, format="json")
        url = reverse("articles:highlight_comment",
                      kwargs={"slug": "slug", "id": 1})
        return url

    def get_slug(self):
        return self.create_article().data['slug']

    def create_bookmark_article(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.client.get(self.get_verify_url(self.user_data))
        return self.client.post(
            self.article_url,
            data=json.dumps(self.valid_article_data),
            content_type='application/json'
        )
