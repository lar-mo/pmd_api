from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from pmd_strings import views

router = routers.DefaultRouter()
router.register('strings/v1', views.StringViewSetv1, basename='string-v1')
router.register('strings/v2', views.StringViewSetv2, basename='string-v2')
router.register('strings/v3', views.StringViewSetv3, basename='string-v3')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('wrapper/', include('api_wrapper.urls'))
]
