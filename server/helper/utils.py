#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import sys, json, types, random, traceback, os, re, hashlib
from datetime import datetime, date, timedelta
from decimal import Decimal

################################################################################
def get_all_functions(module):
    functions = {}
    for f in [module.__dict__.get(a) for a in dir(module) if isinstance(module.__dict__.get(a), types.FunctionType)]:
        functions[f.__name__] = f
    return functions

def getRandomString(size=8):
    import string
    return ''.join(random.choice(string.ascii_letters+string.digits) for i in range(size))

def getRandomLowers(size=8):
    import string
    return ''.join(random.choice(string.ascii_lowercase+string.digits) for i in range(size))

def getRandomNumber(size=8):
    import string
    return ''.join(random.choice(string.digits) for i in range(size))


################################################################################
def checklen(pwd,length=8):
    return len(pwd)>=int(length)

def checkContainUpper(pwd):
    return bool(re.match('.*[A-Z]',pwd))

def checkContainNum(pwd):
    return bool(re.match('.*[0-9]',pwd))

def checkContainNotNum(pwd):
    return bool(re.match('.*[^0-9]',pwd))

def checkContainLower(pwd):
    return bool(re.match('.*[a-z]',pwd))

def checkSymbol(pwd):
    return bool(re.match('.*[^0-9A-Za-z]',pwd))

def get_sha1(string1):
    return hashlib.sha1(string1.encode('utf8')).hexdigest()

def get_md5(string1):
    return hashlib.md5(string1.encode('utf8')).hexdigest()

def n10to62(value):
    stc = '0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(stc)
    retval = ''
    intp, remp = divmod(value,length)
    while intp>0:
        retval = stc[remp]+retval
        intp, remp = divmod(intp,length)
    retval = stc[remp]+retval
    return retval

def n62to10(value):
    stc = '0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    length = len(stc)
    retval = 0
    for x in range(len(value)):
        retval = retval+stc.find(value[x])*length**(len(value)-x-1)
    return retval

def n16to62(value):
    return n10to62(int(value, 16))

def n36to10(value):
    stc = '0123456789abcdefghigklmnopqrstuvwxyz'
    length = len(stc)
    retval = 0
    for x in range(len(value)):
        retval = retval+stc.find(value[x])*length**(len(value)-x-1)
    return retval

def copy_dict(sd, keys=[]):
    import copy
    if not keys:
        return copy.copy(sd)
    else:
        return dict([(key, val) for key, val in sd.items() if key in keys])

