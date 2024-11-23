import re
from rest_framework import serializers
from car.models import Brand, Country, Comments, Car

def validate_comment(value):
    if not re.search(r'^[^\[\]*%&!=\';`]*$', value):
        raise serializers.ValidationError({"comment": "Not valid letters in comment"})


class CountrySerializer(serializers.ModelSerializer):
    brands = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Country
        fields = ['id','name','brands']
        read_only_fields = ['id']


class BrandSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField(read_only=True)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), write_only=True )
    cars = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    country_info = serializers.SlugRelatedField(read_only=True, slug_field='name', source='country')

    class Meta:
        model = Brand
        fields = ['id','name', 'country','country_info', 'cars','comments_count']

    def get_comments_count(self, instance):
        return Comments.objects.filter(car__brand=instance).count()


class CarSerializer(serializers.ModelSerializer):
    brand_info = serializers.SlugRelatedField(read_only=True, slug_field='name', source='brand')
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), write_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    comments = serializers.SlugRelatedField( read_only=True, slug_field='comment', many=True)

    class Meta:
        model = Car
        fields = ['id', 'name','brand','start_year','end_year',
                  'brand_info', 'comments_count', 'comments']


class CommentsSerializer(serializers.ModelSerializer):
    car = serializers.PrimaryKeyRelatedField(queryset=Car.objects.all(), write_only=True)
    about_car = serializers.SlugRelatedField(read_only=True, slug_field='name', source='car')

    class Meta:
        model = Comments
        fields = ['id', 'email','created','comment', 'car', 'about_car']
        read_only_fields = ['id','created']

    def validate(self,data):
        validate_comment(data['comment'])
        return data
