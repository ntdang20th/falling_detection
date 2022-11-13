from django.urls import path, include
from .views import FollowUpView, ResponesData
urlpatterns = [
    path('', FollowUpView.as_view(), name='flup'),
    path('post/', ResponesData)
]
