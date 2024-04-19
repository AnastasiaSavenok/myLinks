from django.db import connection
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.links.models import Link, Collection
from .serializers import LinkSerializer, UpdateLinkRequestSerializer, \
    ListLinkSerializer, CreateLinkSerializer, CollectionListSerializer, CollectionCreateSerializer, \
    CollectionDetailSerializer, CollectionAddLinkSerializer

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


class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionDetailSerializer
    permission_classes = [IsAuthenticated, IsVerified]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionCreateSerializer
        elif self.action == 'list':
            return CollectionListSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return CollectionCreateSerializer
        elif self.action == 'add_link' or self.action == 'remove_link':
            return CollectionAddLinkSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'add_link' or self.action == 'remove_link' or self.action == 'retrieve':
            queryset = queryset.prefetch_related('links')
        return queryset

    @action(detail=True, methods=['post'])
    def add_link(self, request, pk=None):
        collection = self.get_object()
        link_id = request.data.get('link_id')

        try:
            link = Link.objects.get(pk=link_id, author=request.user)
        except Link.DoesNotExist:
            return Response({'detail': 'Link not found.'}, status=404)

        collection.links.add(link)
        serializer = CollectionDetailSerializer(collection)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['post'])
    def remove_link(self, request, pk=None):
        collection = self.get_object()
        link_id = request.data.get('link_id')

        try:
            link = Link.objects.get(pk=link_id, author=request.user)
        except Link.DoesNotExist:
            return Response({'detail': 'Link not found.'}, status=404)

        collection.links.remove(link)
        serializer = CollectionDetailSerializer(collection)
        return Response(serializer.data, status=200)


class TopUsersView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''
            SELECT
                cu.email,
                lc.website,
                lc.book,
                lc.article,
                lc.music,
                lc.video,
                lc.count_links
            FROM
                users_customuser cu
            LEFT JOIN
                (
                    SELECT 
                        author_id,
                        COUNT(CASE WHEN link_type = 'website' THEN 1 END) AS website,
                        COUNT(CASE WHEN link_type = 'book' THEN 1 END) AS book,
                        COUNT(CASE WHEN link_type = 'article' THEN 1 END) AS article,
                        COUNT(CASE WHEN link_type = 'music' THEN 1 END) AS music,
                        COUNT(CASE WHEN link_type = 'video' THEN 1 END) AS video,
                        COUNT(*) AS count_links
                    FROM 
                        links_link
                    GROUP BY 
                        author_id
                ) lc ON cu.id = lc.author_id
            ORDER BY
                lc.count_links DESC, 
                cu.date_joined ASC
            LIMIT 10;
            ''')

            data = cursor.fetchall()
        result = [
            {
                "email": row[0],
                "website": row[1],
                "book": row[2],
                "article": row[3],
                "music": row[4],
                "video": row[5],
                "count_links": row[6]
            }
            for row in data
        ]

        return Response(result)
