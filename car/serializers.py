import base64
import re

from django.utils.encoding import force_str
from rest_framework import serializers
from car.models import Country, Publisher, Comments, Game, Studio


def validate_comment(value):
    if not re.search(r'^[^\[\]*%&!=\';`]*$', value):
        raise serializers.ValidationError({"comment": "Not valid letters in comment"})


class CountrySerializer(serializers.ModelSerializer):
    publishers = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Country
        fields = ['id','name','publishers']
        read_only_fields = ['id']


class PublisherSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True )
    # game = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    country_info = serializers.SlugRelatedField(read_only=True, slug_field='name', source='country')

    class Meta:
        model = Publisher
        fields = ['id','name', 'country','country_info','founded', 'comments_count']

    def get_comments_count(self, instance):
        return Comments.objects.filter(game__publisher=instance).count()


class StudioSerializer(serializers.ModelSerializer):
    country_info = serializers.SlugRelatedField(read_only=True,source='country', slug_field='name')
    country = serializers.PrimaryKeyRelatedField( queryset=Country.objects.all(), write_only=True)

    class Meta:
        model = Studio
        fields = ['name', 'country', 'country_info']

class GameSerializer(serializers.ModelSerializer):
    studio_info = serializers.SlugRelatedField(read_only=True, slug_field='name', source='games_studios')
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all(), write_only=True)
    publisher_info = serializers.SlugRelatedField(read_only=True, slug_field='name', source='games_publishers')
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), write_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = serializers.SlugRelatedField( read_only=True, slug_field='comment', many=True)

    class Meta:
        model = Game
        fields = ['id', 'name','studio', 'studio_info','publisher', 'publisher_info', 'release_year',
                  'dls_count','preview',  'comments_count', 'comments']


class CommentsSerializer(serializers.ModelSerializer):
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all(), write_only=True)
    about_game = serializers.SlugRelatedField(read_only=True, slug_field='name', source='game')
    preview_game = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'email','created','comment', 'game', 'about_game', 'preview_game']
        read_only_fields = ['id','created']

    def validate(self,data):
        validate_comment(data['comment'])
        return data

    def get_preview_game(self, obj):
        if obj.game and obj.game.preview:
            return obj.game.preview.url
        return None
