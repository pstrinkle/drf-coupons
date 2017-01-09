from django.apps import apps
from django.utils.timezone import now
from rest_framework import serializers

from coupons.models import Coupon, ClaimedCoupon


class CouponSerializer(serializers.ModelSerializer):
    """
    RW Coupon serializer.
    """

    def validate(self, data):
        """
        Verify the input used to create or update the coupon is valid.  Because we don't support PATCH for the binding
        field, we don't need to check self.instance for this.
        """

        # Verify if the expiration date is set that it's in the future.
        if 'expires' in data:
            if data['expires'] < now():
                raise serializers.ValidationError("Expiration date set in the past.")

        # Verify if it's type is 'percentage' that the percentage value is set
        # Verify if it's type is 'value' that the value is set.
        if data['type'] == 'percent':
            if 'value' in data and data['value'] > 1.0:
                raise serializers.ValidationError("Percentage discount specified greater than 100%.")

        # Verify if it's bound, that the user exists or the email is valid.
        if 'bound' in data and data['bound']:
            if data['bind'] == 'user':
                if 'binding_user' not in data:
                    raise serializers.ValidationError("Bound to user, but binding_user field not specified.")
            elif data['bind'] == 'email':
                if 'binding_email' not in data:
                    raise serializers.ValidationError("Bound to email, but binding_email field not specified.")

        return data

    def validate_code(self, value):
        """
        An explicit check here, because it was just throwing:
        IntegrityError: UNIQUE constraint failed: coupons_coupon.code_l and not returning 400.
        """

        if Coupon.objects.filter(code_l=value.lower()).count() > 0:
            raise serializers.ValidationError("Coupon code violate uniqueness constraint.")

        return value

    def create(self, validated_data):
        validated_data['code_l'] = validated_data['code'].lower()

        coupon = Coupon.objects.create(**validated_data)

        return coupon

    class Meta:
        model = apps.get_model('coupons.Coupon')
        fields = ('created', 'updated', 'code',
                  'code_l', 'type', 'expires',
                  'bound', 'bind', 'binding_email',
                  'binding_user', 'repeat', 'value',
                  'id')


class ClaimedCouponSerializer(serializers.ModelSerializer):
    """
    RW ClaimedCoupon serializer.
    """

    class Meta:
        model = apps.get_model('coupons.ClaimedCoupon')
        fields = ('redeemed', 'coupon', 'id')

