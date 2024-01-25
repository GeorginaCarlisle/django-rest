from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        # Above creates a new instance of the serializer of the profiles
        # Many=True needed to specify we're serializing multiple Profile instances
        return Response(serializer.data)
