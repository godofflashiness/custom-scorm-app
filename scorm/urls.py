from django.urls import path, include
from .views import test_dropdown

urlpatterns = [
    path('test_dropdown/', test_dropdown, name='test_dropdown'),
]
