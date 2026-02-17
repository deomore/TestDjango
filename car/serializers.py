import base64
import re

from django.utils.encoding import force_str
from rest_framework import serializers
from car.models import Country, Publisher, Comments, Game, Studio, News, Category


def validate_comment(value):
    if not re.search(r'^[^\[\]*%&!=\';`]*$', value):
        raise serializers.ValidationError({"comment": "Not valid letters in comment"})

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']

class PublisherSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source='country', read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'country', 'country_details', 'founded', 'comments_count']

    def get_comments_count(self, instance):
        return Comments.objects.filter(game__publisher=instance).count()

class StudioSerializer(serializers.ModelSerializer):
    country_details= CountrySerializer(source='country', read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True)

    class Meta:
        model = Studio
        fields = ['id', 'name', 'country', 'country_details']


class GameSerializer(serializers.ModelSerializer):
    studio_details = StudioSerializer(source='studio', read_only=True)
    publisher_details = PublisherSerializer(source='publisher', read_only=True)
    categories_details = CategorySerializer(source='categories', many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    # Поля ДЛЯ ЗАПИСИ СО СТОРОНЫ ФРОНТА
    studio = serializers.PrimaryKeyRelatedField(queryset=Studio.objects.all(), write_only=True)
    publisher = serializers.PrimaryKeyRelatedField(queryset=Publisher.objects.all(), write_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, write_only=True)

    class Meta:
        model = Game
        fields = [
            'id', 'name', 'description', 'studio', 'studio_details',
            'publisher', 'publisher_details', 'categories', 'categories_details',
            'release_year', 'dls_count', 'preview', 'comments_count'
        ]

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

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
