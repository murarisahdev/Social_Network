from django.urls import include, path

from friends.views import (AcceptedFriendListView, FriendRequestCreateAPIView,
                           FriendRequestUpdateAPIView,
                           PendingFriendRequestListView)

urlpatterns = [
    path('friend-request/create/', FriendRequestCreateAPIView.as_view(), name='friend-request-create'),
    path('friend-request/<int:pk>/update/', FriendRequestUpdateAPIView.as_view(), name='friend-request-update'),
    path('friend-request/pending/', PendingFriendRequestListView.as_view(), name='list-pending-friend-requests'),
    path('friend-request/accepted/', AcceptedFriendListView.as_view(), name='list-accepted-friend-requests')
]
