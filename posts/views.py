
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    View to return a list of all posts
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to return a specific post where pk will be the id of the post
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.all()
