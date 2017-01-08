from django.apps import apps
from rest_framework import serializers

from coupons.models import *


class CouponSerializer(serializers.HyperlinkedModelSerializer):
    """
    RW Coupon serializer.
    """

    class Meta:
        model = apps.get_model('coupons.Coupon')
        fields = ('created', 'updated', 'code',
                  'code_l', 'type', 'expires',
                  'bound', 'bind', 'binding',
                  'repeat', 'id')


class ClaimedCouponSerializer(serializers.HyperlinkedModelSerializer):
    """
    RW ClaimedCoupon serializer.
    """

    class Meta:
        model = apps.get_model('coupons.ClaimedCoupon')
        fields = ('redeemed', 'coupon', 'id')

