from typing import Any

import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from users import views as users_views


schema_view: Any = get_schema_view(
    openapi.Info(
        title='4Challenge API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('api/', include(
        [
            path('admin/', admin.site.urls),
            path('docs/', schema_view.with_ui('swagger')),
            path('token/', users_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
            path('token/refresh/', users_views.CustomTokenRefreshView.as_view(), name='token_refresh'),
        ]
    )),
]

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
