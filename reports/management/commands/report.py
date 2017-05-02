from django.core.management import BaseCommand
 #The class must be named Command, and subclass BaseCommand
import matplotlib.pyplot as plt
from reports.models import ostPerfHistory
import datetime
from pytz import timezone
import numpy as np

class Command(BaseCommand):
# Show this when the user types help
    help = "Generates SVG charts for Lustre throuhput values."
    min_throughput = 160
    start_date = 0
    end_date = 0


    # A command must define handle()
    def handle(self, *args, **options):
        berlin = timezone('Europe/Berlin')
        self.start_date = datetime.datetime(2017,4,2,0,0,0, tzinfo=berlin)
        self.end_date = datetime.datetime(2017,4,7,23,59,59, tzinfo=berlin)
        mid = self.start_date+datetime.timedelta(days=((self.end_date-self.start_date).days/2)+0.5)

        self.stdout.write(self.style.WARNING("Rendering"), ending="\n")

        x,y = self.main_overview()
        self.renderOverview(x, y, mid)


        dates, throughputs = self.getDataForOsts()
        for ostname,v in dates.iteritems():
            self.renderOst(v, throughputs[ostname], mid, ostname)


    def main_overview(self):
        latest_question_list = ostPerfHistory.objects.filter(throughput__lte=160*1024*1024, timepoint__range=(self.start_date, self.end_date)).order_by('timepoint')
        output = "\n".join([q.ost+" "+str(q.timepoint.strftime('%Y-%m-%d %H:%M:%S %Z%z'))+" "+str(q.throughput/1024/1024)+" MB" for q in latest_question_list])
        throughputs, dates = [], []
        for q in latest_question_list:
            dates.append(q.timepoint)
            throughputs.append(q.throughput/1024/1024)
        #self.stdout.write("Doing All The Things!"+output)
        return (dates, throughputs)

    def getDataForOsts(self):
        result = list(ostPerfHistory.objects.filter(throughput=0, timepoint__range=(self.start_date, self.end_date)).order_by('timepoint').values_list('ost', flat=True))
        print result
        latest_question_list = ostPerfHistory.objects.filter(ost__in=result, timepoint__range=(self.start_date, self.end_date)).order_by('timepoint')
        #output = "\n".join([q.ost+" "+str(q.timepoint.strftime('%Y-%m-%d %H:%M:%S %Z%z'))+" "+str(q.throughput/1024/1024)+" MB" for q in latest_question_list])
        dates, throughputs = {}, {}
        for q in latest_question_list:
            ostname=q.ost
            if not (ostname in dates or ostname in throughputs):
                dates[ostname] = []
                throughputs[ostname] = []
            dates[ostname].append(q.timepoint)
            throughputs[ostname].append(q.throughput/1024/1024)
        #self.stdout.write("Doing All The Things!"+output)
        return (dates, throughputs)


    def renderOverview(self, x,y, mid):
        self.stdout.write(" - Overview.svg", ending="")
        z=np.array(y)
        lines = plt.plot(x, y, 'b.', x, z*0+self.min_throughput, 'r--')
        plt.text(mid, 165, 'OSTs with Throughput Values lower than 160 MB/s', horizontalalignment='center')
        plt.xlim(self.start_date, self.end_date)
        plt.ylim(0, 180)
        plt.ylabel('min-throughput (MB/s)')
        plt.xlabel('date OST')
        plt.gca().set_position([0, 0, 1, 1])
        #plt.axis([0, 7, 0, 200])
        plt.axis('on')
        plt.savefig("tmp/Overview.svg", format="svg", bbox_inches='tight')
        plt.clf()
        self.stdout.write(self.style.SUCCESS("     - done"), ending="\n")


    def renderOst(self, x,y, mid, ostname):
        self.stdout.write(' - '+ostname+'.svg', ending='')
        z=np.array(y)
        lines = plt.plot(x, y, 'k', x, z*0+self.min_throughput, 'r--')
        plt.text(mid, 165, r'Throughput Values lower than 160 MB/s', horizontalalignment='center')
        plt.xlim(self.start_date, self.end_date)
        plt.ylim(0, 2400)
        plt.grid(True)
        plt.ylabel('Throughput (MB/s)')
        plt.xlabel('Fig.: '+ostname)
        plt.gca().set_position([0, 0, 1, 1])
        #plt.axis([0, 7, 0, 200])
        plt.axis('on')
        plt.savefig("tmp/"+ostname+".svg", format="svg", bbox_inches='tight')
        plt.clf()
        self.stdout.write(self.style.SUCCESS("     - done"), ending="\n")
