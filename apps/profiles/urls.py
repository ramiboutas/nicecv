from django.urls import path

from .views import crop_photo
from .views import delete_child
from .views import delete_photo_files
from .views import delete_profile
from .views import order_child_formset
from .views import profile_create
from .views import profile_list
from .views import profile_update
from .views import update_child_formset
from .views import upload_photo
from .views import update_profile_fields
from .views import update_settings


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
    path("delete/profile/<uuid:id>/", delete_profile, name="delete"),
    # delete child (obj from formset)
    path("delete-object/<str:klass>/<int:id>/", delete_child, name="delete-child"),
    # update child formset
    path("formset/<str:klass>/<uuid:id>/", update_child_formset, name="update-formset"),
    # update profile field
    path("update-fields/<uuid:id>/", update_profile_fields, name="update-fields"),
    # update settings forms
    path("settings/<str:klass>/<uuid:id>/", update_settings, name="update-settings"),
    # order child formset
    path("order/<str:klass>/<uuid:id>/", order_child_formset, name="order-formset"),
    # upload photo
    path("upload-photo/<uuid:id>/", upload_photo, name="upload-photo"),
    # crop potho
    path("crop-photo/<uuid:id>/", crop_photo, name="crop-photo"),
    # delete photos files
    path("delete-photos/<uuid:id>/", delete_photo_files, name="delete-photos"),
]
