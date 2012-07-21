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
    v = v_str.split('||')
    req,res = {},{}
    for zv in v:
        if zv == '':
            continue
        zvv = json.loads(zv)
        # 2012-07-20 22:46:55.922075
        t = dt.strptime(zvv[2],"%Y-%m-%d %H:%M:%S.%f")
        data = [t, zvv[3]]
        if zvv[0] == "req":
            req[zvv[1]] = data
        elif zvv[0] == "res":
            res[zvv[1]] = data
        else:
            continue
    paired = {}
    timedelta = []
    for k,v in req.items():
        reqobj = v
        try:
            resobj = res[k]
        except KeyError:
            #skip unpaired
            continue
        paired[k] = [reqobj,resobj]
        td = (resobj[0]-reqobj[0]).microseconds
        timedelta.append([v[1],
                          td,
                          int((td*1.0/1000.0)),
                          k,
                          ])
    #dthandler = lambda obj: obj.isoformat() if isinstance(obj, dt) else None
    #return HttpResponse(json.dumps(timedelta, default=dthandler),mimetype='application/json')
    #return HttpResponse(json.dumps(timedelta),mimetype='application/json')
    timedelta.sort(key=lambda x: x[0])
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
