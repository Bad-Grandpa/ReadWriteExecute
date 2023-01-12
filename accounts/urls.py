from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LJUserLoginForm

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LJUserLoginForm
    ), name='login'),
]
