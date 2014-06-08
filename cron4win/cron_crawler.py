#!/usr/bin/env python
# -*- coding: UTF-8 -*-
 
import sched, time
from threading import Thread, Timer
import subprocess
import sys
 
# IP:219.224.135.124
START_ID = 5000000
END_ID = 10000000

s = sched.scheduler(time.time, time.sleep)

class Job(Thread):
    def __init__(self, since_id, hourly_jobs):
        super(Job, self).__init__()
        self.since_id = since_id
        self.hourly_jobs = hourly_jobs

    def run(self):
        '''主要业务执行方法'''
        print_time()
        if since_id > END_ID:
            print 'crawl out of max range id'
        elif since_id < START_ID:
            print 'crawl out of min range id'
        else:
            theproc = subprocess.Popen("python scrapy_script.py %s %s" % (self.since_id, self.since_id + self.hourly_jobs), shell = True)
            theproc.communicate()


def each_day_time(hour,min,sec,next_day=True):
    '''返回当天指定时分秒的时间'''
    struct = time.localtime()
    if next_day:
        day = struct.tm_mday + 1
    else:
        day = struct.tm_mday
    return time.mktime((struct.tm_year,struct.tm_mon,day,
        hour,min,sec,struct.tm_wday, struct.tm_yday,
        struct.tm_isdst))
    
def print_time(name="None"):
    print name, ":","From print_time",\
        time.time()," :", time.ctime()
 

def do_somthing(since_id, hourly_jobs):
    delay = 3600 - time.time() % 3600
    s.enter(delay, 0, do_somthing, (since_id + hourly_jobs, hourly_jobs))
    print "-------------- auto scrapy begin running from %s to %s --------------" % (since_id, since_id + hourly_jobs)
    job = Job(since_id, hourly_jobs)
    job.start()  

 
def main(since_id, hourly_jobs):
    #指定相对时间delay后执行任务
    priority = 0
    delay = 0
    s.enter(delay, priority, do_somthing, (since_id, hourly_jobs))
    s.run()


if __name__ == "__main__":
    since_id = int(sys.argv[1])
    hourly_jobs = 30000
    main(since_id, hourly_jobs)
