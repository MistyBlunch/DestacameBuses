from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path, include
from .routers import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('plataforma.urls')),
    path('api/', include(router.urls)),
    path('chofer', TemplateView.as_view(template_name='index.html')),
]
