from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from AppServer.urls import views as vw_appS

urlpatterns = (
    [
        path('admin/', admin.site.urls),
        path('webservice/', include('WebService.urls')),
        
        path('', vw_appS.vwIndex),
        path('appserver/', include('AppServer.urls')),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
