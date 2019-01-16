"""
JWT configuration
"""
from rest_framework_jwt.settings import api_settings


"""
By default, django-restframework--jwt generates a token
here we create a function to manually create a token
with user data of our choosing
Here the token is passed the user email
All the the jwt configurations are defined globally in the project settings.py
"""


def get_jwt_token(user):
    """
    Creates a token manually
    more info: https://getblimp.github.io/django-rest-framework-jwt/
    """
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)
