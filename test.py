import datetime
from django.core.management import BaseCommand
 #The class must be named Command, and subclass BaseCommand
import matplotlib.pyplot as plt
from reports.models import ostPerfHistory
from django.utils import timezone

latest_question_list = ostPerfHistory.objects.order_by('-throughput')[:5]
dt=latest_question_list[0]
for dt in latest_question_list:
    print "timepoint: "+((dt.timepoint).strftime("%s"))
    print "timedelta: "+(timezone.now()-datetime.timedelta(days=1)).strftime("%s")
    if dt.is_recent():
        print(dt.timepoint.strftime("%Y-%m-%d %H:%M:%S") + ": true")
    else:
        print(dt.timepoint.strftime("%Y-%m-%d %H:%M:%S") + ": false")

exit()
