from django.utils import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Inherit the PasswordResetTokenGenerator class.
# Override the make_hash_value


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_verified)
        )


# instance of the TokenGenerator class.
account_activation_token = TokenGenerator()
