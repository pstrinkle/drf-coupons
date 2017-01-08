from __future__ import unicode_literals

from django.db import models

COUPON_TYPES = (
    ('percent', 'percent'),
    ('value', 'value'),
)

BINDING_TYPES = (
    ('user', 'user'),
    ('email', 'email'),
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

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # The coupon code itself (so it can be mixed case in presentation... meh)
    code = models.CharField(max_length=64)
    # the lowercase version to simplify some code (for now).
    code_l = models.CharField(max_length=64)

    # Whether it's a percentage off or a value.
    type = models.CharField(max_length=16, choices=COUPON_TYPES)

    # When it expires (if it expires)
    expires = models.DateTimeField()

    # Is this coupon bound to a specific user?
    bound = models.BooleanField(default=False)
    bind = models.CharField(max_length=16, choices=BINDING_TYPES, default='user')
    binding = models.CharField(max_length=256, blank=True, null=True)
    # We'll validate the binding's value based on the type, either it's an int that is a user's pk or a valid email
    # string.  You'll be able to query for coupons with a binding value that's a pk, because you can just provide an
    # int via the URL query string and it should process it properly.

    # How many times this coupon can be used, -1 == infinitely, otherwise it's a number, such as 1 or many.
    # To determine if you can redeem it, it'll check this value against the number of corresponding ClaimedCoupons.
    repeat = models.IntegerField(default=-1)

    # single-use per user
    # repeat = 1, bound = True, binding = user_id
    # single-use globally
    # repeat = 1, bound = False

    # infinite-user per user
    # repeat = -1, bound = True
    # infinite globally
    # repeat = -1, bound = False

    # specific number of times per user
    # repeat => 0, bound = True, binding = user_id
    # specific number of times globally
    # repeat => 0, bound = False


class ClaimedCoupon(models.Model):
    """
    These are the instances of claimed coupons, each is an individual usage of a coupon by someone in the system.
    """

    redeemed = models.DateTimeField(auto_now_add=True)

    # Every claimed coupon should point back to a Coupon in the system.
    coupon = models.ForeignKey('Coupon')


