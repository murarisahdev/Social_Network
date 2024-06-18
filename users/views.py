from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password != confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'user': self.get_serializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class LoginView(APIView):
    """
    Login API View
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        serializer = CustomUserSerializer(user)  # Use your existing serializer or create a new one for login response
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })



class SearchUsersView(generics.ListAPIView):
    """
    Search Users API View
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CustomUserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if not query:
            return CustomUser.objects.none()

        if '@' in query:
            return CustomUser.objects.filter(email__iexact=query)
        else:
            return CustomUser.objects.filter(first_name__icontains=query) | \
                   CustomUser.objects.filter(last_name__icontains=query)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
