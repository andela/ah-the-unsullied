from rest_framework import serializers

# Local application imports
from .models import UserProfile


class ProfileSerialiazer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.ImageField()
    following = serializers.SerializerMethodField()

    def get_following(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return None
        user_to_check = request.user.profiles
        status = user_to_check.check_if_following(obj)
        return status

    class Meta:
        model = UserProfile
        fields = ['username', 'image', 'bio', 'following']
        read_only_fields = ('created_at', 'updated_at', 'username')
