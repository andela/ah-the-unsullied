from django.test import TestCase

from authors.apps.authentication.models import User


class TestAuthModel(TestCase):
    """Test the user model"""

    def test_user_creation(self):
        User.objects.create_user(
            username='Monster', email='drink@drink.com', password='hdfhfhhdf34W!'
        )
        monster = User.objects.get(username='Monster')
        self.assertEqual(monster.username, 'Monster')

    def test_super_user_creation(self):
        User.objects.create_superuser(
            username='Monster', email='drink@drink.com', password='hdfhfhhdf34W!'
        )
        monster = User.objects.get(username='Monster')
        self.assertEqual(monster.username, 'Monster')
