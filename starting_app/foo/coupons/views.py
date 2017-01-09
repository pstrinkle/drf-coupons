from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from coupons.models import Coupon
from coupons.serializers import CouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets a user manipulate their folders.
    """

    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

