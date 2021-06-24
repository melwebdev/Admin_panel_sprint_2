from django.contrib import admin
from django.urls import path
from django.urls import include
import config.settings.base as settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
    SHOW_TOOLBAR_CALLBACK = True
