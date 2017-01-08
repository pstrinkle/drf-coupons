from __future__ import unicode_literals

from django.db import models

COUPON_TYPES = (
    ('discount', 'discount'),
    ('value', 'value'),
)


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

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # The coupon code itself (so it can be mixed case in presentation... meh)
    code = models.CharField(max_length=64)
    # the lowercase version to simplify some code (for now).
    code_l = models.CharField(max_length=64)

    # Whether it's a percentage off or a value.
    type = models.CharField(choices=COUPON_TYPES)


class ClaimedCoupon(models.Model):
    """
    These are the instances of claimed coupons, each is an individual usage of a coupon by someone in the system.
    """

    added = models.DateTimeField(auto_now_add=True)

    # Every claimed coupon should point back to a Coupon in the system.
    coupon = models.ForeignKey('Coupon')


