import requests
from bs4 import BeautifulSoup
from rest_framework import serializers
from src.links.models import Link, LinkType, Collection


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = [
            'uuid',
            'title',
            'description',
            'url',
            'image',
            'link_type',
            'created_at',
            'updated_at',
            'author'
        ]


class ListLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('uuid', 'url',)


class UpdateLinkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('title', 'description', 'image', 'link_type', 'updated_at')
        read_only_fields = ('updated_at',)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.link_type = validated_data.get('link_type', instance.link_type)
        instance.save()
        return instance


class CreateLinkSerializer(serializers.ModelSerializer):
    url = serializers.CharField(required=True)

    class Meta:
        model = Link
        fields = ('url',)

    def create(self, validated_data):
        url = validated_data['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)})

        title = soup.find('meta', {'property': 'og:title'})
        title = title['content'] if title else ''
        if not title:
            title = soup.title.string if soup.title else ''

        description = soup.find('meta', {'property': 'og:description'})
        description = description['content'] if description else ''
        if not description:
            description = soup.find('meta', {'name': 'description'})
            description = description['content'] if description else ''
        image = soup.find('meta', {'property': 'og:image'})
        image = image['content'] if image else ''

        link_type = LinkType.WEBSITE
        if 'book' in url:
            link_type = LinkType.BOOK
        elif 'article' in url or 'blog' in url:
            link_type = LinkType.ARTICLE
        elif 'music' in url or 'spotify' in url:
            link_type = LinkType.MUSIC
        elif 'video' in url or 'watch' in url:
            link_type = LinkType.VIDEO

        data = {
            'title': title,
            'description': description,
            'url': url,
            'image': image,
            'link_type': link_type,
            'author': self.context['request'].user
        }

        return Link.objects.create(**data)


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description')


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('title', 'description')


class CollectionDetailSerializer(serializers.ModelSerializer):
    links = ListLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('title', 'description', 'links')


class CollectionAddLinkSerializer(serializers.ModelSerializer):
    links = ListLinkSerializer(many=True, read_only=True)
    link_id = serializers.CharField(required=True)

    class Meta:
        model = Collection
        fields = ('link_id', 'title', 'description', 'links')
        read_only_fields = ('title', 'description', 'links')
