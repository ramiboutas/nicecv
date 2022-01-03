from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import hx_create_object_view
from .views import hx_upload_full_photo_view, hx_get_photo_modal_view, hx_crop_photo_view


urlpatterns = [
    # general
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('hx-create-object/', hx_create_object_view, name='profiles_create_object_url'),

    # htmx - photo
    path('hx-upload-full-photo/<uuid:pk>/', hx_upload_full_photo_view, name='profiles_upload_full_photo_url'),
    path('hx-get-photo-modal/<uuid:pk>/', hx_get_photo_modal_view, name='profiles_get_photo_modal_url'),
    path('hx-crop-photo/<uuid:pk>/', hx_crop_photo_view, name='profiles_crop_photo_url'),


]
