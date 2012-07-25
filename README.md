djangotracer
============

Django Tracer gives you actionable insights into the working of your Django application to help you tune it. 

License
-------
Read the file "LICENSE" distributed with this project

Installation
------------
1. ```cd``` to the your Django project directory that contains your Django apps. We'll refer to this directory as ```PrjDir``` from now
1. Place djangotracer app there by executing ```git clone git://github.com/kirubakaran/djangotracer.git```
1. Add ```'PrjDir.djangotracer'``` to INSTALLED_APPS in settings.py of your project
1. Add ```'PrjDir.djangotracer.middleware.InsightMiddleware'``` to MIDDLEWARE_CLASSES in settings.py of your project
1. Add ```url(r'^tracer/', include('PrjDir.djangotracer.urls')),``` to urls.py of your project
1. Install the following packages
   1. python-memcached
1. Run ```python manage.py syncdb```
1. You can access the app at http://[your url]/tracer

Feedback
--------
Please send me your feedback at djangotracer@kirubakaran.com I'd love to hear from you. Thanks!