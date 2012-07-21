from django.http import HttpResponse,HttpResponseRedirect
import json

import pylibmc
mc = pylibmc.Client(['127.0.0.1:11211'])

def home(request):
    v_str = mc.get('djangotracer')
    v = v_str.split('||')
    return HttpResponse(json.dumps(v),mimetype='application/json')


