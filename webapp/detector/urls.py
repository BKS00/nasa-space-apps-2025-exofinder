from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('results/<int:pk>/', views.results, name='results'),
    path('model-info/', views.model_info, name='model_info'),
]

