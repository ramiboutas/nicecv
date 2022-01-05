from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import hx_create_object_view, hx_delete_object_view
from .views import hx_upload_full_photo_view, hx_crop_photo_view, hx_delete_photos_view
from .views import hx_get_photo_modal_view, hx_remove_photo_modal_view


urlpatterns = [
    # general
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('hx-create-object/', hx_create_object_view, name='profiles_create_object'),

    # htmx - object - delete
    path('hx-delete-object/<uuid:pk>/', hx_delete_object_view, name='profiles_delete_object'),

    # htmx - photo
    path('hx-upload-full-photo/<uuid:pk>/', hx_upload_full_photo_view, name='profiles_upload_full_photo'),
    path('hx-crop-photo/<uuid:pk>/', hx_crop_photo_view, name='profiles_crop_photo'),
    path('hx-delete-photos/<uuid:pk>/', hx_delete_photos_view, name='profiles_delete_photos'),

    # htmx - photo modal
    path('hx-get-photo-modal/<uuid:pk>/', hx_get_photo_modal_view, name='profiles_get_photo_modal'),
    path('hx-remove-photo-modal/<uuid:pk>/', hx_remove_photo_modal_view, name='profiles_remove_photo_modal'),


]
