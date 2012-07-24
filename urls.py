from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mainprj.djangotracer',
    url('^$', 'views.home', name='tracerhome'),
    url('^persist$', 'views.persist', name='tracerpersist'),
    url('^reset$', 'views.reset', name='tracerreset'),
    )
