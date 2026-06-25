from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.urls import include, re_path
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db import connection

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

def health(request: HttpRequest) -> HttpResponse:
    connection.ensure_connection()
    return HttpResponse("ok")


urlpatterns = [
    re_path(r'^health/$', health, name='health'),
    re_path(r'^django-admin/', admin.site.urls),

    re_path(r'^admin/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),

    re_path(r'^search/$', search_views.search, name='search'),
    re_path(r'^random/$', search_views.random, name='random'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    re_path(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
