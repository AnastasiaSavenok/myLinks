from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from src.links.models import Link
from .serializers import LinkSerializer, UpdateLinkRequestSerializer, \
    ListLinkSerializer, CreateLinkSerializer

from src.core.permissions import IsVerified, IsOwner


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticated, IsVerified, IsOwner]

    def get_object(self):
        lookup_field = self.lookup_field
        lookup_url_kwarg = self.lookup_url_kwarg or lookup_field
        filter_kwargs = {lookup_field: self.kwargs[lookup_url_kwarg]}
        return self.get_queryset().get(**filter_kwargs)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateLinkSerializer
        elif self.action == 'list':
            return ListLinkSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UpdateLinkRequestSerializer
        return self.serializer_class

    def get_queryset(self):
        return Link.objects.filter(author=self.request.user)
