"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import (path, re_path, include)
from myapp.home import views
from myapp.item import urls
from myqpp.item.views import (error403, error404, error500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.index),
    re_path(r'^product\/', include((urls.extra_patterns, 'item')), name='product'),
    re_path(r'^products', include((urls.urlpatterns, 'item')), name='products'),
]

# override default handler with jsonResponse
handler403 = error403
handler404 = error404
handler500 = error500