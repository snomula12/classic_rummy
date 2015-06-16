from django.conf.urls import patterns, include, url

from django.contrib import admin
from classic_rummy.views import ClassisRummyView
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from classic_rummy import settings

admin.autodiscover()


urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^classic/rummy/', ClassisRummyView.as_view()),
    url(r'^draw/card/', "classic_rummy.views.draw_card"),
    url(r'^update/player/card/', "classic_rummy.views.update_player_cards"),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
