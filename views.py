from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from django.shortcuts import render_to_response

import json
import os
from datetime import datetime as dt

import pylibmc
mc = pylibmc.Client(['127.0.0.1:11211'])

def home(request):
    v_str = mc.get('djangotracer')
    timedelta = []
    if v_str != None:
        v = v_str.split('||')
        for zv in v:
            if zv == '':
                continue
            zvv = json.loads(zv)
            timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
            treq = dt.strptime(zvv['reqts'],timestamp_format)
            tres = dt.strptime(zvv['rests'],timestamp_format)
            elapsed = (tres - treq).microseconds
            zvv['elapsed'] = elapsed
            zvv['elapsed_pixels'] = int(zvv['elapsed']*1.0/1000.0)
            timedelta.append(zvv)

    timedelta.sort(key=lambda x: x['path'])
    data = {
        'timedelta':timedelta,
        }
    template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'templates/home.html')
    tstr = open(template_file,'r').read()
    t = Template(tstr)
    c = Context(data)
    return HttpResponse(t.render(c))

def reset(request):
    mc.delete('djangotracer')
    return HttpResponse('ok')
