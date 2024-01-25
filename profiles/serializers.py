from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # Above overwrites owner to be username and not id (as it is in profile model)

    class Meta:
        """
        The mechanism that Django uses to parameterize or modify the class creation process.
        """
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image'
        ]