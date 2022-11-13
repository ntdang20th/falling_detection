from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('patient/', include('patient.urls')),
    path('address/', include('address.urls')),
    path('device/', include('device.urls')),
    path('doctor/', include('doctor.urls')),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get-token/', TokenObtainPairView.as_view(), name='get-token'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('verify-token/', TokenVerifyView.as_view(), name='verify-token'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
