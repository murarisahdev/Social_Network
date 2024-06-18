from django.urls import path

from users.views import LoginView, RegisterView, SearchUsersView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('search/', SearchUsersView.as_view(), name='search-users')
]
