#!/usr/bin/env python
#-*- encoding: utf-8 -*-

import os, sys, base64, time, traceback, json, random, importlib, hashlib
import web, yaml, redis

web.config.vars = web.Storage({
    'option': web.Storage({}),
})
variant = web.config.vars

from helper import formator, utils, console

def loadConfig(config_filename):
    variant['cfgfile'] = config_filename
    print(os.path.abspath(variant['cfgfile']))
    variant['option'] = web.Storage(yaml.load(open(variant['cfgfile']).read(), Loader=yaml.FullLoader))

render_globals = utils.get_all_functions(formator)
render = web.template.render('../www', cache=not web.config.debug, globals=render_globals)

def get_render(inpath, view=render):
    return getattr(view, inpath) or web.notfound

def get_client_ip():
    ipaddress = web.ctx.env.get('HTTP_X_FORWARDED_FOR', '').split(',')[0] or web.ctx.env.get('HTTP_X_REAL_IP', web.ctx.env.get('REMOTE_ADDR', 'UnknownClientIP'))
    return ipaddress

web.config.vars['get_render'] = get_render
