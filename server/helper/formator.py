#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys, json, random, traceback
from datetime import datetime, date, timedelta
import time, calendar
from decimal import Decimal

class DateTimeJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, Decimal):
            return "%.2f" % obj
        elif isinstance(obj, timedelta):
            s = str(obj)
            if len(s)==7:
                s = '0'+s
            return s
        else:
            try:
                return json.JSONEncoder.default(self, obj)
            except:
                return str(obj)

def json_string(obj,pretty=False,ensure_ascii=True,cls=None):
    if cls is None:
        cls = DateTimeJSONEncoder
    if pretty:
        return json.dumps(obj,cls=cls,ensure_ascii=ensure_ascii,indent=4)
    else:
        return json.dumps(obj,cls=cls,ensure_ascii=ensure_ascii,separators=(',',':'))

def json_object(text, default={}):
    try:
        return json.loads(text) if text else default
    except Exception as e:
        return default

def isFloat(v):
    try:
        v = float(v)
        return True
    except Exception as e:
        return False

def shuffle(*args, **keywords):
    return random.shuffle(*args, **keywords)

def getDatetimeStrFromTimestamp(t=None):
    # timestamp to yyyy-mm-dd hh:mm:ss
    import time
    retval = int(t) if t else int(time.time())
    if str(retval).isdigit():
        try:
            retval = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(retval)))
        except Exception as e:
            pass
    return retval

def getYYYYMMDDFromTimestamp(t=None):
    # timestamp to yyyy-mm-dd
    import time
    retval = int(t) if t else int(time.time())
    if str(retval).isdigit():
        try:
            retval = time.strftime("%Y%m%d", time.localtime(float(retval)))
        except Exception as e:
            pass
    return retval

def get_datetime_from_ts(timestamp, offset=0):
    try:
        return datetime.fromtimestamp(float(timestamp)+offset)
    except Exception as e:
        traceback.print_exc()
        return datetime.fromtimestamp(time.time()+offset)

def date_add(days,d=None):
    if not d: d = datetime.today()
    return d + timedelta(days=days)

def month_add(months,ts=None,oday=0):
    d = datetime.fromtimestamp(ts if ts else time.time())
    nm = d.month + months
    ny = d.year
    nd = max(d.day, oday)
    while nm > 12:
        nm = nm - 12
        ny = ny + 1
    while nm < 0:
        nm = nm + 12
        ny = ny - 1
    if nm in (4,6,9,11):
        if nd == 31:
            nd = 30
    elif nm in (2,):
        isleap = is_leap_year(ny)
        if nd in (30, 31):
            nd = 29 if isleap else 28
        elif nd == 29 and not isleap:
            nd = 28
    return datetime(ny, nm, nd, d.hour, d.minute, d.second, d.microsecond).timestamp()

def is_leap_year(year_num):
    if year_num % 100 == 0:
        if year_num % 400 == 0:
            return True
        else:
            return False
    else:
        if year_num % 4 == 0:
            return True
        else:
            return False

def get_ts_from_utcstr(dstr):
    # '2020-04-30T16:58:52.124604525Z' -> 1588265932.0
    # '2020-07-07T02:16:00.673039482+08:00' -> 1594059360.0
    # '2020-07-06T19:39:43.133292713-07:00' -> 1594089583.0
    try:
        d, dstr = dstr.split('T', 1)
        t, dstr = dstr.split('.', 1)
        if dstr.find('+')>0:
            z = '+'+dstr.split('+', 1)[1]
        elif dstr.find('-')>0:
            z = '-'+dstr.split('-', 1)[1]
        elif dstr.find('Z')>0:
            z = '+00:00'
        else:
            z = ''
        dt = datetime.fromisoformat('%sT%s%s'%(d, t, z))
        # return (dt-datetime(year=1970,month=1,day=1)).total_seconds()
        return dt.timestamp()
    except Exception as e:
        traceback.print_exc()
        return 0

def get_utcstr_from_ts(ts):
    # 1588265932.0 -> '2020-04-30T16:58:52.0+00:00'
    # 1594059360.0 -> '2020-07-06T18:16:00.0+00:00'
    # 1594089583.0 -> '2020-07-07T02:39:43.0+00:00'
    return '%s.%s+00:00'%(time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(ts)), datetime.fromtimestamp(ts).microsecond)

