import random
import string
from django.utils.text import slugify


def get_unique_slug(model_instance, slugable_field_name, slug_field_name):

    slug = slugify(getattr(model_instance, slugable_field_name))
    unique_slug = slug
    extension = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=5))
    model_class = model_instance.__class__

    while model_class._default_manager.filter(
            **{slug_field_name: unique_slug}
    ).exists():
        unique_slug = '{}-{}'.format(slug, extension)
    return unique_slug
