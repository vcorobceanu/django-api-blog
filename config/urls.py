# from django.contrib import admin
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.common.helpers import schema_view
from config import settings

urlpatterns = [
    path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('common/', include("apps.common.urls")),
    path('blog/', include("apps.blog.urls")),
    path('users/', include("apps.users.urls")),
    path('task/', include("apps.task.urls")),
    path('TaskManager/', include("TaskManager.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
