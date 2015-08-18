# coding:utf-8
import re
import time
import datetime
import redis
import sys
import os

input = sys.argv[-1]
rds = redis.Redis(host='redis-logcount.yg.hunantv.com', port=8889)
log_list = []
if input == '1':
    file = datetime.date.today()
    log_list.append('/mfs/logs/eru/odan/web-macvlan/' + str(file) + '.log')
elif input == '2':
    log_list = os.list("/mfs/logs/eru/odan/web-macvlan")
else:
    filename = '/mnt/mfs/logs/eru/odan/web-macvlan/' + input
with open(filename) as f:
    date = ''
    for line in f:
        t = re.search(r'^\[([\d-]+\s+[\d:]+)', line)
        if t:
            datetime = time.strptime(t.group(1), '%Y-%m-%d %H:%M:%S')
            timestamp = '%s' % time.mktime(datetime)
            if not date:
                date = time.strftime('%Y-%m-%d', datetime)
            rds.hincrby(date, timestamp, 1)
    data = rds.hgetall(date)
    for key in sorted(data.keys()):
        print key, data[key]
