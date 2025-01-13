from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('chat/', include('chat.urls')),
    #path('selif/', include('file_display.urls')), # Include your app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files  # Include the URLs from the chat app

# Serve media and static files during development
if settings.DEBUG:  # Only serve media and static files in development
    # Serve media files from MEDIA_ROOT
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Serve static files from STATICFILES_DIRS (for development only)
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        # In case STATICFILES_DIRS is empty or not defined, add a fallback to default static path
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
