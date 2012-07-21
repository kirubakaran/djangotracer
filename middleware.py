from datetime import datetime as dt
import os
import base64
import json

import pylibmc
mc = pylibmc.Client(['127.0.0.1:11211'])

class InsightMiddleware(object):
    def __init__(self):
        pass
    
    def process_request(self, request):
        global mc
        uid = base64.urlsafe_b64encode(os.urandom(16))
        now = "%s"%(dt.now(),)
        insertmc('req',uid,now,request.path)
        request.uniq_req_id = uid
        #print "request %s at %s"%('req_'+uid,now,)
        return None

    def process_response(self, request, response):
        global mc
        try:
            uid = request.uniq_req_id
        except:
            return response
        now = "%s"%(dt.now(),)
        insertmc('res',uid,now,request.path)
        #print "response %s at %s"%(uid,now)
        return response

def insertmc(action,uid,data,path):
    global mc
    v_str = mc.get('djangotracer')
    add = json.dumps([action,uid,data,path])    
    if v_str == None:
        v_str = add
    else:
        v_str += "||"+add    
    mc.set('djangotracer',v_str)
    return
