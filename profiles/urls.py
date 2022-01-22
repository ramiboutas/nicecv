from django.urls import path

from .views import ProfileListView, ProfileUpdateView, ProfileCreateView
from .views import create_object_view, delete_object_view
from .views import upload_full_photo_view, crop_photo_view, delete_photos_view
from .views import get_photo_modal_view, remove_photo_modal_view
from .views import save_general_and_contact_info_view
from .views import add_website_object_view, update_website_object_view, delete_website_object_view
from .views import add_skill_object_view, update_skill_object_view, delete_skill_object_view
from .views import add_language_object_view, update_language_object_view, delete_language_object_view




# general

urlpatterns = [
    path('', ProfileListView.as_view(), name='profiles_list'),
    path('list/', ProfileListView.as_view(), name='profiles_list'),
    path('new/', ProfileCreateView.as_view(), name='profiles_new'),
    path('profile/<uuid:pk>/', ProfileUpdateView.as_view(), name='profiles_update'),

    # htmx - object - create
    path('create-object/profile/', create_object_view, name='profiles_create_object'),

    # htmx - object - delete
    path('delete-object/profile/<uuid:pk>/', delete_object_view, name='profiles_delete_object'),
]


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


# general_and_contact_info
urlpatterns += [
        # htmx - general_and_contact_info
        path('save-general-and-contact-info/<uuid:pk>/',
        save_general_and_contact_info_view,
        name='profiles_save_general_and_contact_info'),
]



# websites
urlpatterns += [

        # htmx - add website object
        path('add-website-object/<uuid:pk>/', add_website_object_view, name='profiles_add_website_object'),

        # htmx - update website object
        path('update-website-object/<uuid:pk_parent>/<int:pk>/', update_website_object_view, name='profiles_update_website_object'),

        # htmx - delete website object
        path('delete-website-object/<uuid:pk_parent>/<int:pk>/', delete_website_object_view, name='profiles_delete_website_object'),

]



# skills
urlpatterns += [
        # htmx - add skill object
        path('add-skill-object/<uuid:pk>/', add_skill_object_view, name='profiles_add_skill_object'),

        # htmx - update skill object
        path('update-skill-object/<uuid:pk_parent>/<int:pk>/', update_skill_object_view, name='profiles_update_skill_object'),

        # htmx - delete skill object
        path('delete-skill-object/<uuid:pk_parent>/<int:pk>/', delete_skill_object_view, name='profiles_delete_skill_object'),

]



# languages
urlpatterns += [

        # htmx - add language object
        path('add-language-object/<uuid:pk>/', add_language_object_view, name='profiles_add_language_object'),

        # htmx - update language object
        path('update-language-object/<uuid:pk_parent>/<int:pk>/', update_language_object_view, name='profiles_update_language_object'),

        # htmx - delete language object
        path('delete-language-object/<uuid:pk_parent>/<int:pk>/', delete_language_object_view, name='profiles_delete_language_object'),

]


from .views import activate_description_view, update_description_view, deactivate_description_view
from .views import insert_description_button_view, remove_description_button_view

# description
urlpatterns += [
        # htmx - activate description
        path('activate-description/<uuid:pk>/', activate_description_view, name='profiles_activate_description'),

        # htmx - update description
        path('update-description/<uuid:pk>/', update_description_view, name='profiles_update_description'),

        # htmx - deactivate description
        path('deactivate-description/<uuid:pk>/', deactivate_description_view, name='profiles_deactivate_description'),

        # htmx - add "add description button"
        path('insert-description-button/<uuid:pk>/', insert_description_button_view, name='profiles_insert_description_activation_button'),

        # htmx - delete "add description button"
        path('remove-description-button/<uuid:pk>/', remove_description_button_view, name='profiles_remove_description_activation_button'),

]



from .views import create_child_object_view, update_child_object_view, delete_child_object_view, copy_child_object_view
from .views import insert_child_new_form_view, remove_child_new_form_view
from .views import move_up_child_object_view, move_down_child_object_view
from .views import activate_child_object_view, deactivate_child_object_view
from .views import insert_child_activation_button_view, remove_child_activation_button_view

# any child object
urlpatterns += [
        # htmx - insert child new form
        path('insert-new-form/<str:child_label>/<uuid:pk>/', insert_child_new_form_view, name='profiles_insert_child_new_form'),

        # htmx - remove child new form
        path('remove-new-form/<str:child_label>/<uuid:pk>/', remove_child_new_form_view, name='profiles_remove_child_new_form'),

        # htmx - create child object
        path('create-object/<str:child_label>/<uuid:pk>/', create_child_object_view, name='profiles_create_child_object'),

        # htmx - update child object
        path('update-object/<str:child_label>/<uuid:pk_parent>/<int:pk>/', update_child_object_view, name='profiles_update_child_object'),


        # htmx - move up child object
        path('move-up-child/<str:child_label>/<uuid:pk_parent>/<int:pk>/', move_up_child_object_view, name='profiles_move_up_child_object'),

        # htmx - move down child object
        path('move-down-child/<str:child_label>/<uuid:pk_parent>/<int:pk>/', move_down_child_object_view, name='profiles_move_down_child_object'),

        # htmx - copy child object
        path('copy-child/<str:child_label>/<uuid:pk_parent>/<int:pk>/', copy_child_object_view, name='profiles_copy_child_object'),

        # htmx - delete child object
        path('delete-child/<str:child_label>/<uuid:pk_parent>/<int:pk>/', delete_child_object_view, name='profiles_delete_child_object'),


        # htmx - activate object
        path('activate-child/<str:child_label>/<uuid:pk>/', activate_child_object_view, name='profiles_activate_child_object'),

        # htmx - deactivate object
        path('deactivate-child/<str:child_label>/<uuid:pk>/', deactivate_child_object_view, name='profiles_deactivate_child_object'),


        # htmx - insert_child_activation_button
        path('insert-child-activation-button/<str:child_label>/<uuid:pk>/', insert_child_activation_button_view, name='profiles_insert_child_activation_button'),

        # htmx - remove_child_activation_button
        path('remove-child-activation-button/<str:child_label>/<uuid:pk>/', remove_child_activation_button_view, name='profiles_remove_child_activation_button'),

]
