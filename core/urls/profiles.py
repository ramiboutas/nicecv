from django.urls import path

from ..views.profiles import create_profile_cv
from ..views.profiles import crop_profile_photo
from ..views.profiles import delete_profile_child
from ..views.profiles import delete_photo_files
from ..views.profiles import profile_delete
from ..views.profiles import order_child_formset
from ..views.profiles import profile_create
from ..views.profiles import profile_list
from ..views.profiles import profile_update
from ..views.profiles import update_child_formset
from ..views.profiles import update_profile_fields
from ..views.profiles import update_settings
from ..views.profiles import upload_profile_photo


urlpatterns = [
    # profile list
    path(
        "profiles/",
        profile_list,
        name="profile_list",
    ),
    # create a profile (redirect)
    path(
        "profile-create/",
        profile_create,
        name="profile_create",
    ),
    # profile update (edit view)
    path(
        "profile/<uuid:id>/",
        profile_update,
        name="profile_update",
    ),
    # delete profile
    path(
        "profile-delete/<uuid:id>/",
        profile_delete,
        name="profile_delete",
    ),
    # delete child (obj from formset)
    path(
        "profile-delete-object/<str:klass>/<int:id>/",
        delete_profile_child,
        name="profile_delete_child",
    ),
    # update child formset
    path(
        "formset/<str:klass>/<uuid:id>/",
        update_child_formset,
        name="profile_update_formset",
    ),
    # update profile field
    path(
        "profile-update-fields/<uuid:id>/",
        update_profile_fields,
        name="profile_update_fields",
    ),
    # update settings forms
    path(
        "profile-settings/<str:klass>/<uuid:id>/",
        update_settings,
        name="profile_update_settings",
    ),
    # order child formset
    path(
        "order/<str:klass>/<uuid:id>/",
        order_child_formset,
        name="profile_order_formset",
    ),
    # upload photo
    path(
        "profile-upload-photo/<uuid:id>/",
        upload_profile_photo,
        name="profile_upload_photo",
    ),
    # crop potho
    path(
        "profile-crop-photo/<uuid:id>/",
        crop_profile_photo,
        name="profile_crop_photo",
    ),
    # delete photos files
    path(
        "profile-delete-photos/<uuid:id>/",
        delete_photo_files,
        name="profile_delete_photos",
    ),
    # create cv
    path(
        "profile-create-cv/<uuid:profile_id>/<int:tex_id>/",
        create_profile_cv,
        name="profile_create_cv",
    ),
]
