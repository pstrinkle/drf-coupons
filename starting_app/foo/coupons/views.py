from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from coupons.models import Coupon, ClaimedCoupon
from coupons.serializers import CouponSerializer, ClaimedCouponSerializer


class CouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you create, delete, retrieve coupons.
    """

    serializer_class = CouponSerializer
    queryset = Coupon.objects.all()

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None, **kwargs):
        """
        This forces it to return a 202 upon success instead of 200.
        """

        queryset = self.get_queryset()
        coupon = get_object_or_404(queryset, pk=pk)

        serializer = CouponSerializer(coupon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['put'])
    def redeem(self, request, pk=None, **kwargs):
        """
        Convenience endpoint for redeeming.
        """

        queryset = self.get_queryset()
        coupon = get_object_or_404(queryset, pk=pk)

        # Maybe should do coupon.redeem(user).
        # if data['expires'] < now():

        data = {
            'coupon': pk,
            'user':   self.request.user.id,
        }

        serializer = ClaimedCouponSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
