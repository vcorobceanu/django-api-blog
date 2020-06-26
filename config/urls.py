
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
    path('task/', include("apps.task.urls")),
    path('TaskManager/', include("TaskManager.urls")),
    url(r'^search/', include(search_index_urls)),
]
