from django.urls import path

from . import views

urlpatterns = [
    path('pmdv1dev/', views.pmdv1dev, name='pmdv1dev'),
    path('pmdv2DevGetStrings/', views.pmdv2DevGetStrings, name='pmdv2DevGetStrings'),
    path('pmdv2ProdGetStrings/', views.pmdv2ProdGetStrings, name='pmdv2ProdGetStrings'),
    path('pmdv3DevGetStrings/', views.pmdv3DevGetStrings, name='pmdv3DevGetStrings'),
    path('pmdv3ProdGetStrings/', views.pmdv3ProdGetStrings, name='pmdv3ProdGetStrings'),
    path('flickrApiGetArrangements/', views.flickrApiGetArrangements, name='flickrApiGetArrangements'),
    path('flickrApiGetContainers/', views.flickrApiGetContainers, name='flickrApiGetContainers'),
    path('flickrApiGetSizes/<int:photo_id>/', views.flickrApiGetSizes, name='flickrApiGetSizes'),
    path('flickrApiGetInfo/<int:photo_id>/', views.flickrApiGetInfo, name='flickrApiGetInfo'),
    path('bloggerApiGetLatestPost/', views.bloggerApiGetLatestPost, name='bloggerApiGetLatestPost')
]
