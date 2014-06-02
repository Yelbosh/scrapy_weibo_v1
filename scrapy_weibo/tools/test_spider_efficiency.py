# -*- coding;utf8 -*-
import time
import pymongo

DB_NAME = 'master_timeline_v1'
TB_NAME = 'master_timeline_user'

client =  pymongo.MongoClient() #default localhost 27017
db = client[DB_NAME]
table = db[TB_NAME]
f = open('efficiency_record.log', 'a')
print >> f, '**'*3, time.strftime('%Y-%m-%d %H:%M:%S'), '**'*3
record = 0
while 1:
    count_start = table.count()
    time.sleep(60)
    count_end = table.count()
    num = count_end - count_start
    if num == 0:
        record += 1
        if record == 3: # db.table has no change 3 times then break
	    break
    print >> f, ('%s : %d per minute' % (TB_NAME, num))
f.close()
