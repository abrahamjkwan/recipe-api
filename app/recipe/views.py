from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from recipe import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage tags in the database"""
    # We only want the ListModel function
    # so we use the GenericViewSet and the relevant Mixin
    # we add authentication_classes and permission_classes
    # to add authentication
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    # in generic viewest, provide a queryset to return
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
