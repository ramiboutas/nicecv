from django.urls import path

from . import views
from .views import profile_list
from .views import profile_create
from .views import profile_update
from .views import delete_object
from .views import update_child_form
from .views import update_child_formset
from .views import update_settings
from .views import create_child_object


# from .views import save_personal_information_view, update_description_view

app_name = "profiles"
# general

urlpatterns = [
    # profile list
    path("", profile_list, name="list"),
    # create a profile (redirect)
    path("create/", profile_create, name="create"),
    # profile update (edit view)
    path("profile/<uuid:id>/", profile_update, name="update"),
    # delete profile
    path("delete/profile/<uuid:id>/", delete_object, name="delete"),
    # update child form
    path("form/<str:klass>/<int:id>/", update_child_form, name="update-form"),
    path("form/<str:klass>/", create_child_object, name="create-child-object"),
    # update child formset
    path("formset/<str:klass>/", update_child_formset, name="update-formset"),
    # update settings form
    path("settings/<str:klass>/<int:id>/", update_settings, name="update-settings"),
]


from .views import upload_full_photo_view, crop_photo_view, delete_photos_view
from .views import get_photo_modal_view, remove_photo_modal_view

# photo
urlpatterns += [
    # htmx - photo
    path(
        "upload-full-photo/<uuid:id>/",
        upload_full_photo_view,
        name="profiles_upload_full_photo",
    ),
    path("crop-photo/<uuid:id>/", crop_photo_view, name="profiles_crop_photo"),
    path("delete-photos/<uuid:id>/", delete_photos_view, name="profiles_delete_photos"),
    # htmx - photo modal
    path(
        "get-photo-modal/<uuid:id>/",
        get_photo_modal_view,
        name="profiles_get_photo_modal",
    ),
    path(
        "remove-photo-modal/<uuid:id>/",
        remove_photo_modal_view,
        name="profiles_remove_photo_modal",
    ),
]
