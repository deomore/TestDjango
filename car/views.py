from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from DjangoTest.renders import ExcelCommentsRenderer, CSVCommentsRenderer
from car.models import Country, Comments, Publisher, Studio, Game
from car.serializers import CountrySerializer,  CommentsSerializer, PublisherSerializer, \
    StudioSerializer, GameSerializer

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def current_user(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email,
    })

class CustomCommentsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.method == 'POST'


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class StudioViewSet(viewsets.ModelViewSet):
    queryset = Studio.objects.all()
    serializer_class = StudioSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly | CustomCommentsAuth]


    @action(detail=False, methods=["get"],
            renderer_classes=[ExcelCommentsRenderer, CSVCommentsRenderer])
    def download(self, request):
        queryset = self.get_queryset()

        now = timezone.now()
        file_name = f"comments_archive_{now:%Y-%m-%d_%H-%M-%S}.{request.accepted_renderer.format}"
        serializer = CommentsSerializer(queryset, many=True)
        return Response(serializer.data,
                        headers={"Content-Disposition": f'attachment; filename="{file_name}"'})
