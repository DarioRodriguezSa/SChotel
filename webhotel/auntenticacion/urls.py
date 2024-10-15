from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView

app_name = "auntenticacion"
urlpatterns = [
    path('auth/login/', login_view, name="login"),
    path("auth/logout/", login_view, name="logout")
]