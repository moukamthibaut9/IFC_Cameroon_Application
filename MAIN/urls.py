from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home' ),
    path('forum/',views.forum,name='forum' ),
    path('services/',views.services,name='services' ),
    path('policy/',views.policy,name='policy' ),
]