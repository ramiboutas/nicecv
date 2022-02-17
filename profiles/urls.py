from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import create_object_view, delete_object_view

from .views import save_personal_information_view, update_description_view, update_field_view
from .views import insert_resume_templates_modal_view, remove_resume_templates_modal_view


# general

urlpatterns = [
    path('', ProfileListView.as_view(), name='profiles_list'),
    # path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('create-object/profile/', create_object_view, name='profiles_create_object'),

    # htmx - object - delete
    path('delete-object/profile/<uuid:pk>/', delete_object_view, name='profiles_delete_object'),

    # htmx - save personal information
    path('save-personal-information/<uuid:pk>/', save_personal_information_view, name='profiles_save_personal_information'),

    # htmx - update description
    path('update-description/<uuid:pk>/', update_description_view, name='profiles_update_description'),

    # htmx - update any field
    path('update-field/<str:label>/<uuid:pk>/', update_field_view, name='profiles_update_field'),

    # htmx - resume templates modal
    path('remove-resume-templates-modal/<uuid:pk>/', remove_resume_templates_modal_view, name='profiles_remove_resume_templates_modal'),
    path('insert-resume-templates-modal/<uuid:pk>/', insert_resume_templates_modal_view, name='profiles_insert_resume_templates_modal'),


]

from .views import upload_full_photo_view, crop_photo_view, delete_photos_view

from .views import get_photo_modal_view, remove_photo_modal_view

# photo
urlpatterns += [
        # htmx - photo
        path('upload-full-photo/<uuid:pk>/', upload_full_photo_view, name='profiles_upload_full_photo'),
        path('crop-photo/<uuid:pk>/', crop_photo_view, name='profiles_crop_photo'),
        path('delete-photos/<uuid:pk>/', delete_photos_view, name='profiles_delete_photos'),

        # htmx - photo modal
        path('get-photo-modal/<uuid:pk>/', get_photo_modal_view, name='profiles_get_photo_modal'),
        path('remove-photo-modal/<uuid:pk>/', remove_photo_modal_view, name='profiles_remove_photo_modal'),
]


from .views import create_child_object_view, update_child_object_view, delete_child_object_view, copy_child_object_view
from .views import insert_child_new_form_view, remove_child_new_form_view
from .views import move_up_child_object_view, move_down_child_object_view


# any child object
urlpatterns += [
        # htmx - insert child new form
        path('insert-new-form/<str:label>/<uuid:pk_parent>/', insert_child_new_form_view, name='profiles_insert_child_new_form'),

        # htmx - remove child new form
        path('remove-new-form/<str:label>/<uuid:pk_parent>/', remove_child_new_form_view, name='profiles_remove_child_new_form'),

        # htmx - create child object
        path('create-object/<str:label>/<uuid:pk_parent>/', create_child_object_view, name='profiles_create_child_object'),

        # htmx - update child object
        path('update-object/<str:label>/<uuid:pk_parent>/<int:pk>/', update_child_object_view, name='profiles_update_child_object'),


        # htmx - move up child object
        path('move-up-child/<str:label>/<uuid:pk_parent>/<int:pk>/', move_up_child_object_view, name='profiles_move_up_child_object'),

        # htmx - move down child object
        path('move-down-child/<str:label>/<uuid:pk_parent>/<int:pk>/', move_down_child_object_view, name='profiles_move_down_child_object'),

        # htmx - copy child object
        path('copy-child/<str:label>/<uuid:pk_parent>/<int:pk>/', copy_child_object_view, name='profiles_copy_child_object'),

        # htmx - delete child object
        path('delete-child/<str:label>/<uuid:pk_parent>/<int:pk>/', delete_child_object_view, name='profiles_delete_child_object'),

]

from .views import activate_child_or_field_view, deactivate_child_or_field_view
from .views import insert_child_activation_button_view, remove_child_activation_button_view

# activate or deactivate of childs or fields
urlpatterns += [

        # htmx - activate object
        path('activate-child-or-field/<str:label>/<uuid:pk_parent>/', activate_child_or_field_view, name='profiles_activate_child_object'),

        # htmx - deactivate object
        path('deactivate-child-or-field/<str:label>/<uuid:pk_parent>/', deactivate_child_or_field_view, name='profiles_deactivate_child_object'),


        # htmx - insert_child_activation_button
        path('insert-activation-button/<str:label>/<uuid:pk_parent>/', insert_child_activation_button_view, name='profiles_insert_child_activation_button'),

        # htmx - remove_child_activation_button
        path('remove-activation-button/<str:label>/<uuid:pk_parent>/', remove_child_activation_button_view, name='profiles_remove_child_activation_button'),

]


from .views import insert_child_or_field_help_modal_view, remove_child_or_field_help_modal_view

# insert or remove help modal
urlpatterns += [

        # htmx - insert help modal
        path('insert-child-or-field-help-modal/<str:label>/<uuid:pk_parent>/', insert_child_or_field_help_modal_view, name='profiles_insert_child_or_field_help_modal'),

        # htmx - remove help modal
        path('remove-child-or-field-help-modal/<str:label>/<uuid:pk_parent>/', remove_child_or_field_help_modal_view, name='profiles_remove_child_or_field_help_modal'),

]
