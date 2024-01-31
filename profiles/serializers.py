from rest_framework import serializers
from .models import Profile
from followers.models import Follow


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # Above overwrites owner to be username and not id (as it is in profile model)
    is_owner = serializers.SerializerMethodField()
    # Above adds a new field with the SerializerMethodField allowing definition of a 
    # custom method ('get_is_owner) to determine the value of the field.
    following_id = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        A custom method that is then used to determine the value of custom field is_owner
        """
        request = self.context['request']
        return request.user == obj.owner
    
    def get_following_id(self, obj):
        """
        A custom method that is used to determine the value of following_id
        It checks if the logged in user is the owner of a Follow object where
        the followed field is the owner of the profile being dealt with.
        If so following_id is given the id of this Follow object. If not it is given a value of none.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follow.objects.filter(owner=user, followed=obj.owner).first()
            return following.id if following else None
        return None

    class Meta:
        """
        The mechanism that Django uses to parameterize or modify the class creation process.
        """
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'content', 'image', 'is_owner', 'following_id',
        ]