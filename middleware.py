from datetime import datetime as dt
import os
import base64
    
class InsightMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, request):
        request.uniq_req_id = base64.urlsafe_b64encode(os.urandom(16))
        print "request %s at %s"%(request.uniq_req_id,dt.now(),)
        return None

    def process_response(self, request, response):
        print "response %s at %s"%(request.uniq_req_id,dt.now(),)
        return response
