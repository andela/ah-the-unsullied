from django.test import TestCase

from authors.apps.authentication.models import User

class TestAuthModel(TestCase):

    def setUp(self):
        User.objects.create(
            username='Monster', email='drink@drink.com', password='hdfhfhhdf34W!')

    def test_user_creation(self):
        monster = User.objects.get(username='Monster')
        self.assertEqual(monster.username,'Monster')
