from django.db.models import Count
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics, permissions, filters
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    View to return a list of all posts
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        # The above counts the number of times a relationship is found between the current post and an instance of comment.
        likes_count=Count('likes', distinct=True)
        # In the above likes is the related name given to the post field in the like model.
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = [
        'comments_count',
        'likes_count',
        'likes__created_at',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to return a specific post where pk will be the id of the post
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        # The above counts the number of times a relationship is found between the current post and an instance of comment.
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
