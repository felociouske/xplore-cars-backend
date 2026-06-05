from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include 
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
