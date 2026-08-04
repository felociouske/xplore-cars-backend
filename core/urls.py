from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import RedirectView
from api.ckeditor_views import upload_file_fixed

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("api/car-tax/", include("car_tax.urls")),
    path("ckeditor5/image_upload/", upload_file_fixed, name="custom_ckeditor5_upload"),
]