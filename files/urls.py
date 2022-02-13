from django.urls import path

from .views import download_pdf_view




urlpatterns = [
    path('pdf/<int:pk>/', download_pdf_view, name='files_download_pdf'),
    # path('download-coverletter/<int:pk>/', download_coverletter_view, name='files_download_coverletter'),
]
