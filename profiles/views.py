from django.db.models import Count
from rest_framework import generics, filters
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


class ProfileList(generics.ListAPIView):
    """
    View to return a list of all profiles.
    Extra fields also provided which count the number of posts created by the profile owner
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        # the above is counting the number of links (through foreign keys, one-to-many relationships etc.) between owner of the profile and post instances across the DB.
        # the __ denotes that the relationship is across more than one table jump
        # distinct=True makes sure that only unique pairs are counted (important as there may be multiple paths between related pairs)
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = {
        'posts_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    }


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    View to return a specific profile where pk will be the id of the profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        posts_count=Count('owner__post', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True),
    )
