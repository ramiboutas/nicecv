from django.urls import path

from .views import profile_create_view
from .views import delete_object_view

from .views import profile_list_view
from .views import profile_update_view
from .views import profile_update_fields_view


# from .views import save_personal_information_view, update_description_view

app_name = "profiles"
# general

urlpatterns = [
    path("", profile_list_view, name="list"),
    path("create/", profile_create_view, name="create"),
    path("profile/<uuid:id>/", profile_update_view, name="update"),
    path("profile/<uuid:id>/", profile_update_fields_view, name="update-fields"),
    path("delete/profile/<uuid:id>/", delete_object_view, name="delete"),
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
