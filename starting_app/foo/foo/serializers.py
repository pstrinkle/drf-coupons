from django.apps import apps
from django.utils.timezone import now
from rest_framework import serializers

from foo.models import MiscItem


class MiscItemSerializer(serializers.ModelSerializer):
    """
    RW MiscItem serializer.
    """

    class Meta:
        model = apps.get_model('foo.MiscItem')
        fields = ('name', 'value', 'id')

