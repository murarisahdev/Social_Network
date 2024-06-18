from rest_framework import serializers

from friends.models import FriendRequest, StatusChoices
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = CustomUserSerializer(read_only=True)
    to_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)
    status = serializers.ChoiceField(choices=StatusChoices.choices, default=StatusChoices.PENDING, read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user', 'status', 'created_at', 'updated_at']

    def create(self, validated_data):
        from_user = self.context['request'].user  # Get the current authenticated user
        to_user = validated_data.pop('to_user')
        status = validated_data.get('status', StatusChoices.PENDING)  # Default status to PENDING if not provided
        friend_request = FriendRequest.objects.create(from_user=from_user, to_user=to_user, status=status)
        return friend_request
    
class FriendRequestUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=StatusChoices.choices)
    from_user = CustomUserSerializer(read_only=True)
    to_user = CustomUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['from_user', 'to_user', 'status', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
