from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "vinton-gray-cerf"
admin.site.site_title = "vinton-gray-cerf Portal"
admin.site.index_title = "Welcome to vinton-gray-cerf"

urlpatterns = [
    path('vinton-gray-cerf/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api/configs/', include('configs.urls')),
    path('api/payees/', include('payees.urls')),
    path('api/payroll/', include('payroll.urls')),
    path('accounts/', include('allauth.urls')), # For Social Login
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
