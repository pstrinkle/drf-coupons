from rest_framework import viewsets

from foo.models import MiscItem
from foo.serializers import MiscItemSerializer


class MiscItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that lets you create, delete, retrieve miscellaneous items.
    """

    serializer_class = MiscItemSerializer
    queryset = MiscItem.objects.all()

