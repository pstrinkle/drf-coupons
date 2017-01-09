from django.shortcuts import get_object_or_404
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

    def update(self, request, pk=None, **kwargs):
        """
        This forces it to return a 202 upon success instead of 200.
        """

        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=pk)

        serializer = CouponSerializer(obj, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

