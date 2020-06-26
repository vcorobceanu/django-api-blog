"""tribes_main URL Configuration

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
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include, url
from TaskManager import urls as search_index_urls

from apps.common.helpers import schema_view

urlpatterns = [
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('common/', include("apps.common.urls")),
    path('blog/', include("apps.blog.urls")),
    path('users/', include("apps.users.urls")),
    path('task/', include("apps.task.urls"), name='task'),
    path('TaskManager/', include("TaskManager.urls")),
    url(r'^search/', include(search_index_urls)),
]
