from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

COUPON_TYPES = (
    ('percent', 'percent'),
    ('value', 'value'),
)

try:
    # In case they specified something else in their settings file, which is quite common.
    user = settings.AUTH_USER_MODEL
except AttributeError:
    # get_user_model isn't working at this point in loading.
    from django.contrib.auth.models import User as user


class Coupon(models.Model):
    """
    These are the coupons that are in the system.

    - Coupons can be a value, or a percentage.
    - They can be bound to a specific user in the system, or an email address (not yet in the system).
    - They can be single-use per user, or single-use globally.
    - They can be infinite per a specific user, or infinite globally.
    - They can be used a specific number of times per user, or globally.
    - (They can be used by a specific list of users?)
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # The coupon code itself (so it can be mixed case in presentation... meh)
    code = models.CharField(max_length=64)
    # the lowercase version to simplify some code (for now).
    #
    # usually blank=True goes with null=True, but in this case, we want the admin to know it's optional, but the
    # database does require it, and it needs to be unique.
    code_l = models.CharField(max_length=64, blank=True, unique=True)

    # Whether it's a percentage off or a value.
    type = models.CharField(max_length=16, choices=COUPON_TYPES)

    # When it expires (if it expires)
    expires = models.DateTimeField(blank=True, null=True)

    # The values (either percentage based, or value based), if percentage based make sure it's no greater than 1.0
    value = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    # Is this coupon bound to a specific user?
    bound = models.BooleanField(default=False)
    user = models.ForeignKey(user, blank=True, null=True)

    # How many times this coupon can be used, 0 == infinitely, otherwise it's a number, such as 1 or many.
    # To determine if you can redeem it, it'll check this value against the number of corresponding ClaimedCoupons.
    repeat = models.IntegerField(default=0)

    # single-use per user
    # repeat = 1, bound = True, binding = user_id
    # single-use globally
    # repeat = 1, bound = False

    # infinite-user per user
    # repeat = 0, bound = True
    # infinite globally
    # repeat = 0, bound = False

    # specific number of times per user
    # repeat => X, bound = True, binding = user_id
    # specific number of times globally
    # repeat => X, bound = False


class ClaimedCoupon(models.Model):
    """
    These are the instances of claimed coupons, each is an individual usage of a coupon by someone in the system.
    """

    redeemed = models.DateTimeField(auto_now_add=True)

    # Every claimed coupon should point back to a Coupon in the system.
    coupon = models.ForeignKey('Coupon')
    user = models.ForeignKey(user)
