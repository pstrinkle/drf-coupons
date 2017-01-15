from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from coupons.filters import CouponFilter
from coupons.models import Coupon, ClaimedCoupon
from coupons.serializers import CouponSerializer, ClaimedCouponSerializer

from django.contrib.auth.decorators import user_passes_test


# https://djangosnippets.org/snippets/1703/
def group_required(api_command):
    """
    This is implemented such that it's default open.
    """

    def in_groups(u):
        if u.is_authenticated():
            # supervisor can do anything
            if u.is_superuser:
                return True

            # coupons have permissions set (I think I may set them by default to remove this check)
            if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
                group_names = settings.COUPON_PERMISSIONS[api_command]

                # but no group specified, so anyone can.
                if len(group_names) == 0:
                    return True

                # group specified, so only those in the group can.
                if bool(u.groups.filter(name__in=group_names)):
                    return True
        return False
    return user_passes_test(in_groups)


class CouponViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you create, delete, retrieve coupons.
    """

    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_class = CouponFilter
    search_fields = ('code', 'code_l')
    serializer_class = CouponSerializer

    def get_queryset(self):
        """
        Return a subset of coupons or all coupons depending on who is asking.
        """

        api_command = 'LIST'
        qs_all = Coupon.objects.all()
        qs_none = Coupon.objects.none()

        if self.request.user.is_superuser:
            return qs_all

        # This is different from the normal check because it's default closed.
        if settings.COUPON_PERMISSIONS and api_command in settings.COUPON_PERMISSIONS:
            group_names = settings.COUPON_PERMISSIONS[api_command]

            # So the setting is left empty, so default behavior.
            if len(group_names) == 0:
                return qs_none

            # group specified, so only those in the group can.
            if bool(self.request.user.groups.filter(name__in=group_names)):
                return qs_all

        return qs_none

    @method_decorator(group_required('CREATE'))
    def create(self, request, **kwargs):
        """
        Create a coupon
        """

        serializer = CouponSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    @method_decorator(group_required('UPDATE'))
    def update(self, request, pk=None, **kwargs):
        """
        This forces it to return a 202 upon success instead of 200.
        """

        queryset = Coupon.objects.all()
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

        queryset = Coupon.objects.all()
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
