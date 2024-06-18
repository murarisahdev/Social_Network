from rest_framework import generics, permissions, status, viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from friends.models import FriendRequest, StatusChoices
from friends.serializers import (FriendRequestSerializer,
                                 FriendRequestUpdateSerializer)
from friends.throttling import FriendRequestThrottleRate


class FriendRequestCreateAPIView(generics.CreateAPIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [FriendRequestThrottleRate]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_user = serializer.validated_data['to_user']
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

        friend_request = serializer.save(from_user=request.user)
        return Response({
            'message': 'Friend request sent successfully.',
            'friend_request': FriendRequestSerializer(friend_request).data
        }, status=status.HTTP_201_CREATED)

class FriendRequestUpdateAPIView(generics.UpdateAPIView):

    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestUpdateSerializer
    pagination_class = PageNumberPagination

    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs['pk'])
        except FriendRequest.DoesNotExist:
            raise NotFound('Friend request not found.')

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.to_user != request.user:
            return Response({'error': 'You are not authorized to update this friend request.'}, status=status.HTTP_403_FORBIDDEN)

        # Use the serializer_class to update the instance
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Friend request updated successfully.',
            'friend_request': serializer.data  # Use serializer.data to get serialized data
        }, status=status.HTTP_200_OK)


class PendingFriendRequestListView(generics.ListAPIView):
    """
    View for listing all friends of User.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status=StatusChoices.PENDING)


class AcceptedFriendListView(generics.ListAPIView):
    """
    View for listing all friends of User.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FriendRequestSerializer
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return FriendRequest.objects.filter(from_user=self.request.user, status=StatusChoices.ACCEPTED)
