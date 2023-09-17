from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# http
urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_management.urls')),
    path('hms/', include('hms.urls')),
    path('ims/', include('ims.urls')),
    path('', include('landing.urls')),
]

# static files for development
urlpatterns += staticfiles_urlpatterns()