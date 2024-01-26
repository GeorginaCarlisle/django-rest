from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

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

    class Meta:
        model = Post
        fields = [
            'owner', 'created_at', 'updated_at', 'title', 'content', 
            'image', 'is_owner', 'profile_id', 'profile-image', 'image_filter',
        ]