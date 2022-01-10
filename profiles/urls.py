from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import hx_create_object_view, hx_delete_object_view
from .views import hx_upload_full_photo_view, hx_crop_photo_view, hx_delete_photos_view
from .views import hx_get_photo_modal_view, hx_remove_photo_modal_view
from .views import hx_save_general_and_contact_info_view
from .views import hx_add_website_object_view, hx_update_website_object_view, hx_delete_website_object_view
from .views import hx_add_skill_object_view, hx_update_skill_object_view, hx_delete_skill_object_view
from .views import hx_add_language_object_view, hx_update_language_object_view, hx_delete_language_object_view
from .views import hx_add_description_view, hx_update_description_view, hx_delete_description_view
from .views import hx_add_add_description_button_view, hx_delete_add_description_button_view
from .views import hx_add_education_object_view, hx_update_education_object_view, hx_delete_education_object_view

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

    # htmx - general_and_contact_info
    path('hx-save-general-and-contact-info/<uuid:pk>/', hx_save_general_and_contact_info_view, name='profiles_save_general_and_contact_info'),

    # htmx - add website object
    path('hx-add-website-object/<uuid:pk>/', hx_add_website_object_view, name='profiles_add_website_object'),

    # htmx - update website object
    path('hx-update-website-object/<uuid:pk_parent>/<int:pk>/', hx_update_website_object_view, name='profiles_update_website_object'),

    # htmx - delete website object
    path('hx-delete-website-object/<uuid:pk_parent>/<int:pk>/', hx_delete_website_object_view, name='profiles_delete_website_object'),

    # htmx - add skill object
    path('hx-add-skill-link-object/<uuid:pk>/', hx_add_skill_object_view, name='profiles_add_skill_object'),

    # htmx - update skill object
    path('hx-update-skill-object/<uuid:pk_parent>/<int:pk>/', hx_update_skill_object_view, name='profiles_update_skill_object'),

    # htmx - delete skill object
    path('hx-delete-skill-object/<uuid:pk_parent>/<int:pk>/', hx_delete_skill_object_view, name='profiles_delete_skill_object'),

    # htmx - add language object
    path('hx-add-language-link-object/<uuid:pk>/', hx_add_language_object_view, name='profiles_add_language_object'),

    # htmx - update language object
    path('hx-update-language-object/<uuid:pk_parent>/<int:pk>/', hx_update_language_object_view, name='profiles_update_language_object'),

    # htmx - delete language object
    path('hx-delete-language-object/<uuid:pk_parent>/<int:pk>/', hx_delete_language_object_view, name='profiles_delete_language_object'),

    # htmx - add description
    path('hx-add-description/<uuid:pk>/', hx_add_description_view, name='profiles_add_description'),

    # htmx - update description
    path('hx-update-description/<uuid:pk>/', hx_update_description_view, name='profiles_update_description'),

    # htmx - delete description
    path('hx-delete-description/<uuid:pk>/', hx_delete_description_view, name='profiles_delete_description'),

    # htmx - add "add description button"
    path('hx-add-add-description-button/<uuid:pk>/', hx_add_add_description_button_view, name='profiles_add_add_description_button'),

    # htmx - delete "add description button"
    path('hx-delete-add-description-button/<uuid:pk>/', hx_delete_add_description_button_view, name='profiles_delete_add_description_button'),

    # htmx - add education object
    path('hx-add-education-link-object/<uuid:pk>/', hx_add_education_object_view, name='profiles_add_education_object'),

    # htmx - update education object
    path('hx-update-education-object/<uuid:pk_parent>/<int:pk>/', hx_update_education_object_view, name='profiles_update_education_object'),

    # htmx - delete education object
    path('hx-delete-education-object/<uuid:pk_parent>/<int:pk>/', hx_delete_education_object_view, name='profiles_delete_education_object'),


]
