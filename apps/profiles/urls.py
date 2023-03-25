from django.urls import path

from . import views

# from .views import save_personal_information_view, update_description_view

app_name = "profiles"
# general

urlpatterns = [
    path("", views.profile_list, name="list"),
    path("create/", views.profile_create, name="create"),
    path("profile/<uuid:id>/", views.profile_update, name="update"),
    path("profile/<uuid:id>/settings/", views.profile_settings, name="settings"),
    path("delete/profile/<uuid:id>/", views.delete_object, name="delete"),
    # child methods
    path("update-child/<str:klass>/<int:id>/", views.update_child, name="update-child"),
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
