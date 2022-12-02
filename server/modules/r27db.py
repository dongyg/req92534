#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, base64, time, traceback, json, random, hashlib, uuid, string
from datetime import datetime, date, timedelta
import yaml, web, redis, pymongo

from config import get_client_ip, variant
from helper import utils, formator

dbsql = variant.get('dbsql', None)
dbrds = variant.get('dbrds', None)
dbmgo = variant.get('dbmgo', None)

################################################################################
def initDBConnection():
    global dbsql, dbrds, dbmgo
    if 'glrds' not in variant and 'redis' in variant['option']:
        dbrds = redis.Redis(**variant['option']['redis'])
        variant.glrds = dbrds
        # variant['option'].pop('redis')
        try:
            variant.glrds.ping()
        except Exception as e:
            traceback.print_exc()
            return False
    if 'dbsql' not in variant and 'mysql' in variant['option']:
        # variant.dbsql = web.database(dbn='mysql', host='127.0.0.1', db='test', user='root', pw='123456')
        dbsql = web.database(**variant['option']['mysql'])
        variant.dbsql = dbsql
        variant['option'].pop('mysql')
        try:
            variant.dbsql.query("select version() version")
        except Exception as e:
            traceback.print_exc()
            return False
    if 'dbmgo' not in variant and 'mongo' in variant['option']:
        variant.dbmgo = dbmgo = pymongo.MongoClient(variant['option']['mongo'])
        try:
            dbmgo.list_database_names()
            initMongoSchema()
        except Exception as e:
            traceback.print_exc()
            return False
    return True

def initMongoSchema():
    clevents = dbmgo["req92534"]["events"]
    clevents.create_index("id")
    clevents.create_index("severity")

def numget(x):
    try: return float(x)
    except: return None

web.numget = numget


################################################################################
def insertEvents(events):
    clevents = dbmgo["req92534"]["events"]
    count = 0
    try:
        for row in events:
            if 'id' not in row: continue
            myquery = {'id': row['id']}
            if list(clevents.find(myquery)):
                clevents.update_one(myquery, {"$set": row})
            else:
                clevents.insert_one(row)
            count += 1
    except:
        pass
    # clevents.estimated_document_count()
    return count

def listEvents(severity, areaid, offset=0, limit=50):
    clevents = dbmgo["req92534"]["events"]
    myquery = {"areas" : {"$elemMatch" : {"id" : areaid}}, 'severity': severity}
    records = list(clevents.find(myquery).limit(limit).skip(offset))
    return records

def insertApiCall(requesturi, clientip):
    # Save API calling from other applications for monitor reasons
    apicalls = dbmgo["req92534"]["apicalls"]
    apicalls.insert_one({"clientip": clientip, "requesturi":requesturi, "ts":time.time()})
