from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BankSystem API",
        default_version='v1',
        description="BankSystem API",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger/$', schema_view.with_ui('swagger')),
    path('api/auth/', include('authentication.urls')),
]
