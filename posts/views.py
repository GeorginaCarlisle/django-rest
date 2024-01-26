from django.http import Http404
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_api.permissions import IsOwnerOrReadOnly


class PostList(APIView):
    """
    View to return a list of all posts
    """
    serializer_class = PostSerializer
    # The above renders a form to the admin interface for creating a new post
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    #IsAuthenticatedOrReadOnly is a built in permission that only allows readonly requests unless logged in

    def get(self, request):
        """
        get method used to handle HTTP GET request for this view
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """
        post method used to handle HTTP POST request for this view
        """
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    """
    View to return a specific post where pk will be the id of the post
    """
    serializer_class = PostSerializer

    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        Gets requested post. Checking permissions first and
        raising an error if the post doesn't exist or permission is not met.
        """
        try:
            post = Post.objects.get(pk=pk)
            self.check_object_permissions(self.request, post)
            # Above is a DRF method which checks if the user associated with the request 
            # has permission to perform the specified action on the given object
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        get method used to send requested post back.
        """
        post = self.get_object(pk)
        # Above calls the get_object method defined above
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        put method used to handle HTTP PUT request for this view and update a post
        """
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        """
        delete method used to handle HTTP DELETE request for this view
        """
