"""madrese URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('', include('index.urls')),
    path('accounts/', include('accounts.urls')),
    path('student/', include('student.urls')),
    path('mentor/', include('mentor.urls')),
    path('manager/', include('manager.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'index.views.error_400'
handler403 = 'index.views.error_403'
handler404 = 'index.views.error_404'
handler503 = 'index.views.error_503'
