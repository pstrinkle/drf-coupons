from rest_framework import viewsets

from coupons.models import Coupon
from coupons.serializers import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets a user manipulate their folders.
    """

    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()
