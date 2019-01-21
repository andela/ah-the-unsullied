from rest_framework import serializers

# Local application imports
from .models import UserProfile


class ProfileSerialiazer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.ImageField()

    class Meta:
        model = UserProfile
        fields = ['username', 'image', 'bio', 'created_at', 'updated_at']
        read_only_fields = ('created_at', 'updated_at', 'username')
