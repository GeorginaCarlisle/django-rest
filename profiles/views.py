from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(APIView):
    """
    View to return a list of all profiles
    """
    def get(self, request):
        """
        get method used to handle HTTP GET request for this view
        """
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={'request': request})
        # Above creates a new instance of the serializer of the profiles
        # Many=True needed to specify we're serializing multiple Profile instances
        return Response(serializer.data)


class ProfileDetail(APIView):
    """
    View to return a specific profile where pk will be the id of the profile
    """
    serializer_class = ProfileSerializer
    # Above explicitly sets the serializer_class attribute so framework automatically renders a form
    # which is based on the fields defined within the ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # Above defines the permissions to be used as part of this view. 
    # These are then called on check_object_permissions
    def get_object(self, pk):
        """
        get_object method used to retrieve a specific object based on
        look up parameters, here the parameter is a 
        primary identifier eg. Primary Key aka pk.
        """
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            # Above is a DRF method which checks if the user associated with the request 
            # has permission to perform the specified action on the given object
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        get method used to handle HTTP GET request for a specified profile
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        put method used to handle HTTP PUT request for a specified profile
        HTTP PUT is typically used to update an existing resource OR
        create a new resource if it doesn't exist.
        Here the request.data is .....
        """
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)