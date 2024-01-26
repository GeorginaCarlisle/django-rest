from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # Above overwrites owner to be username and not id (as it is in profile model)
    is_owner = serializers.SerializerMethodField()
    # Above the SerializerMethodField allows definition of a custom method ('get_is_owner)
    # to determine the value of the field. 

    def get_is_owner(self, obj):
        """
        A custom method that is then used to determine the value of custom field is_owner
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        """
        The mechanism that Django uses to parameterize or modify the class creation process.
        """
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner'
        ]