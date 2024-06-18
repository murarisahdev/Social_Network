from rest_framework.throttling import UserRateThrottle


class FriendRequestThrottleRate(UserRateThrottle):
    """
    Throttle class to limit the rate of friend requests.

    This class limits the rate of friend requests made by a user. It inherits from the `UserRateThrottle` class provided by Django REST Framework.
    # Returns '3/min'
    """
    rate = '3/min'