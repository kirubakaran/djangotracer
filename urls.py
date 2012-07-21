from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mainprj.djangotracer',
    url('^.*$', 'views.home', name='tracerhome'),
    )
