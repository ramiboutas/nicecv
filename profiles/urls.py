from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import hx_create_object_view
from .views import hx_upload_and_crop_photo_view, hx_upload_full_photo_view


urlpatterns = [
    # general
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('hx-create-object/', hx_create_object_view, name='profiles_create_object_url'),

    # htmx - upload photo
    path('hx-upload-and-crop-photo/<uuid:pk>/', hx_upload_and_crop_photo_view, name='profiles_upload_and_crop_photo_url'),

    path('hx-upload-full-photo/<uuid:pk>/', hx_upload_full_photo_view, name='profiles_upload_full_photo_url'),


]
