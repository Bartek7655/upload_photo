from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('upload-photo/', views.ImageUploadView.as_view(), name='upload-photo'),
    path('list-photo/', views.ListImageView.as_view(), name='list-photo'),
    path('get-binary-image/<int:pk>/', views.BinaryImageGetView.as_view(), name='get-binary-photo'),
]
