from datetime import datetime as dt
import json

# trying memcache because i was occasionally getting errors with pylibmc
# and people think python-memcached is the solution
# https://lists.infrae.com/pipermail/silva-dev/2011q3/002241.html
import memcache
mc = memcache.Client(['127.0.0.1:11211'])

class TracerStore(object):
    def __init__(self):
        self.reqts = None
        self.rests = None
        return

    def setreqts(self):
        self.reqts = dt.now()
        return

    def setrests(self):
        self.rests = dt.now()
        return

    def getstate(self):
        if self.reqts == None or self.rests == None:
           return None
        else:
            timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
            return {
                'reqts'   : self.reqts.strftime(timestamp_format),
                'rests'   : self.rests.strftime(timestamp_format),
            }

class InsightMiddleware(object):
    def __init__(self):
        pass
    
    def process_request(self, request):
        if request.path.find('/tracer') == 0: return None
        t = TracerStore()
        t.setreqts()
        request.djangotracer = t
        return None

    def process_response(self, request, response):        
        try:
            t = request.djangotracer
        except:
            return response
        t.setrests()
        state = t.getstate()        
        if state != None:
            state['path'] = request.path
            insertmc(state)
        return response

def insertmc(state):
    global mc
    n1 = dt.now()
    v_str = mc.get('djangotracer')
    add = json.dumps(state)
    if v_str == None:
        v_str = add
    else:
        v_str += "||"+add    
    mc.set('djangotracer',v_str)
    n2 = dt.now()
    print "memcache overhead = %s microseconds"%((n2-n1).microseconds,)
    return
