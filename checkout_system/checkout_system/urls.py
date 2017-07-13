from django.conf.urls import url, include
from django.contrib import admin
from ads import urls as ads_urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ads/', include(ads_urls))
]
