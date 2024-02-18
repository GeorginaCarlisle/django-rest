from rest_framework import serializers
from .models import Post
from likes.models import Like

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    comments_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def validate_image(self, value):
        """
        A custom validation method for the image field 
        where value is the value saved in the image field.
        Size is saved in bytes with the below calculation representing 2mbs
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger tahn 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger tahn 4096px'
            )
        return value


    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner
    
    def get_like_id(self, obj):
        """
        A custom method to determine the like_id value
        It checks if the logged in user is the owner of a like object where
        the post is this post. If so like_id is given the id of this like object.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            liked = Like.objects.filter(owner=user, post=obj). first()
            return liked.id if liked else None
        return None

    class Meta:
        model = Post
        fields = [
            'owner', 'created_at', 'updated_at', 'title', 'content', 
            'image', 'is_owner', 'profile_id', 'profile_image', 'image_filter',
            'like_id', 'comments_count', 'likes_count', 'id'
        ]