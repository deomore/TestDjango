from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from DjangoTest.renders import ExcelCommentsRenderer, CSVCommentsRenderer
from car.models import Country, Brand, Car, Comments
from car.serializers import CountrySerializer, BrandSerializer, CarSerializer, CommentsSerializer


class CustomCommentsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.method == 'POST'


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly | CustomCommentsAuth]


    @action(detail=False, methods=["get"], renderer_classes=[ExcelCommentsRenderer, CSVCommentsRenderer])
    def download(self, request):
        queryset = self.get_queryset()

        now = timezone.now()
        file_name = f"comments_archive_{now:%Y-%m-%d_%H-%M-%S}.{request.accepted_renderer.format}"
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data, headers={"Content-Disposition": f'attachment; filename="{file_name}"'})
