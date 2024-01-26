from django.shortcuts import render
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status, permissions


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

    def get(self, request):
        """
        get method used to handle HTTP GET request for this view
        """
    def put(self, request):
        """
        put method used to handle HTTP PUT request for this view and update a post
        """
    def delete(self, request):
        """
        delete method used to handle HTTP DELETE request for this view
        """
