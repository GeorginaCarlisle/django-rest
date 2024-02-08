from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    """
    ListCreateAPIView: Provides get and post method handlers.
    It also automatically sends the request through to the serializer as part of the context.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    # Above queryset is used to define which records need pulling from the DB
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'post'
        # Above retrieves all the comments associated with a given post.
    ]

    def perform_create(self, serializer):
        """
        This methiod is a hook provided by the 'CreateAPIView' and 'CreateModelMixin' classes
        The later being extend by ListCreateAPIView. It allows for customisation
        of the new object before it is saved to the database.
        """
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView: Used for read-write-delete endpoints to represent a single model instance.
    Provides get, put, patch and delete method handlers.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()