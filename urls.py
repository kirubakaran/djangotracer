from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mainprj.djangotracer',
    url('^$', 'views.home', name='tracerhome'),
    url('^reset$', 'views.reset', name='tracerreset'),
    )
