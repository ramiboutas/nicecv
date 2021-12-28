from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import hx_create_object_view

urlpatterns = [
    # general
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('hx-create-object/', hx_create_object_view, name='profiles_hx_create_object_url'),


    # save profile data, save skill ... whatever
]
