from django.urls import path
from graphene_django.views import GraphQLView
from . import views

urlpatterns = [
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('ergazomenoi/<int:pk>/edit/',
         views.ErgUpdateView.as_view(), name='erg_edit'),
    path('ergazomenoi/new/', views.ErgCreateView.as_view(), name='erg_new'),
    # path('ergazomenoi/<int:pk>/', views.ErgDetailView.as_view(), name='erg_detail'),
    path('ergazomenoi/<int:pk>/', views.ErgUpdateView.as_view(), name='erg_detail'),
    path('ergazomenoi/', views.ErgListView.as_view(), name='erg'),
    path('misthodosies/<int:pk>/', views.MisDetailView.as_view(), name='mis_detail'),
    path('misthodosies/', views.MisListView.as_view(), name='mis'),
    path('apd/<int:apd_id>/', views.apd2zip, name='apd2zip'),
    path('apd/', views.ApdListView.as_view(), name='apd'),
    path('fmy/', views.FmyListView.as_view(), name='fmy'),
    path('fmy/<int:fmy_id>/', views.fmy2zip, name='fmy2zip'),
    path('', views.HomePageView.as_view(), name='home'),
    path("graphql", GraphQLView.as_view(graphiql=True), name='graphql'),
]
