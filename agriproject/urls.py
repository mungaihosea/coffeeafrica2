from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

namespace = "transactions"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("accounts.urls", "accounts"), namespace="accounts")),
    path(
        "transactions/",
        include(("transactions.urls", "transactions"), namespace="transactions"),
    ),
    path("feedback/", include(("feedback.urls", "feedback"), namespace="feedback")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

