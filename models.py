from django.db import models

class TraceData(models.Model):
    path      = models.CharField(max_length=255)
    reqts     = models.DateTimeField()
    rests     = models.DateTimeField()
    elapsed   = models.IntegerField() #microseconds
    version   = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s took %s microsec"%(self.path,self.elapsed)
