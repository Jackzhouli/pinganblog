"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from cnblong import views
from django.views.static import serve
from blog import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cnblog/', include(('cnblong.urls', 'cnblong'), namespace='test')),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    re_path('^$', views.index),
    path('register/', views.register, name='register'),
    path('get_valid_img/', views.get_validcode_img),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
