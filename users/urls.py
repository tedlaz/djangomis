from django.urls import path
from django.views.generic.base import TemplateView
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    # path('login/', views.LogInView.as_view(), name='login'),
    path('', TemplateView.as_view(template_name='users/home.html'))
]
