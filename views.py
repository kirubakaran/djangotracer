from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template, Context
from django.shortcuts import render_to_response
from django.db import transaction

import json
import os
from datetime import datetime as dt

import memcache
mc = memcache.Client(['127.0.0.1:11211'])

import models

def home(request):
    v_str = mc.get('djangotracer')
    persist(request)
    d = models.TraceData.objects.all()
    rrdata = []
    for dd in d:
        rrdata.append({
            'path':dd.path,
            'elapsed':dd.elapsed,
            'elapsed_pixels':dd.elapsed*1.0/1000.0,
            })
    data = {
        'rrdata':rrdata,
        }
    template_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                            'templates/home.html')
    tstr = open(template_file,'r').read()
    t = Template(tstr)
    c = Context(data)
    return HttpResponse(t.render(c))

def reset(request):
    global mc
    mc.delete('djangotracer')
    return HttpResponse('ok')

def persist(request):
    global mc
    v_str = mc.get('djangotracer')
    if v_str == None: return HttpResponse('empty')
    v = v_str.split('||')
    with transaction.commit_manually():
        try:
            for zv in v:
                if zv == '': continue
                zvv = json.loads(zv)
                timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
                reqts = dt.strptime(zvv['reqts'],timestamp_format)
                rests = dt.strptime(zvv['rests'],timestamp_format)
                elapsed = (rests - reqts).microseconds
                td = models.TraceData(
                    path=zvv['path'],
                    reqts=reqts,
                    rests=rests,
                    elapsed=elapsed,
                    )
                td.save()
        except Exception, e:
            transaction.rollback()
            return HttpResponse('error: "%s" on zv=%s'%(e,zv))
        else:
            v_str_new = mc.get('djangotracer')
            mc.set('djangotracer', v_str_new[len(v_str):])
            transaction.commit()
            return HttpResponse('ok')
