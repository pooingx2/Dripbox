from django.conf.urls import patterns, include, url
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',

    #url(r'^hello/', hello),
    url(r'^$', main),
    url(r'^main/', main),
    url(r'^signup/', signup),
    url(r'^login/', login),
    url(r'^home/', home),
    url(r'^user/', user),
    url(r'^logout/', logout),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
