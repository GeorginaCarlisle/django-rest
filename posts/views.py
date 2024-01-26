from django.shortcuts import render
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response


class PostList(APIView):
    """
    View to return a list of all posts
    """
    def get(self, request):
        """
        get method used to handle HTTP GET request for this view
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    def post():
        """
        post method used to handle HTTP POST request for this view
        """

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
