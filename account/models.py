from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    nickname=models.CharField(max_length=20, default='new user')

    def __str__(self):
        return 'User({}): {}'.format(self.id, self.nickname)

    def as_dict(self):
        d = {
            'id':self.id,
            'phone':self.username,
            'nickname':self.nickname
        }
        return d