from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    is_tenant = models.BooleanField(default=False, help_text='When this is true at creation time, this user becomes a '
                                                             'tenant under the main')
    REQUIRED_FIELDS = ['username']

    class Hasura:
        track = True


class UserProxy(User):
    """Create methods and functions over the user model here"""

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        proxy = True

