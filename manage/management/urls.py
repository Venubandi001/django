from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views  
from django.conf.urls.static import static

urlpatterns = [
    path('hello/', views.hello, name='hello'),
     path('management_data/', views.display_json_data, name='management_data'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)