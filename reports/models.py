import datetime
from django.utils import timezone

from django.db import models


class ostPerfHistory(models.Model):
    class Meta:
        db_table = 'OST_PERF_HISTORY'

    timepoint = models.DateTimeField('date published')
    ost = models.CharField(max_length=7)
    ip = models.CharField(max_length=15)
    write_bytes = models.BigIntegerField()
    throughput = models.BigIntegerField()
    duration = models.IntegerField()

    def __unicode__(self):
        return unicode(self.ost)

    def is_recent(self):
        now = timezone.now()
        return (timezone.now() - datetime.timedelta(days=1))<=self.timepoint<=now
