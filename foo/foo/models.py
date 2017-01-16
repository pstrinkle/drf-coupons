from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class MiscItem(models.Model):
    """
    These are the instances of claimed coupons, each is an individual usage of a coupon by someone in the system.
    """

    name = models.CharField(max_length=64)
    value = models.IntegerField()
