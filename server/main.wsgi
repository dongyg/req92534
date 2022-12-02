#!/usr/bin/env python
#-*- encoding: utf-8 -*-

# Written Assignment Phase Req#92534 ISL 27R – Full Stack Developer

# Set work path
import os, sys, _thread, signal
app_root = os.path.dirname(__file__)
if app_root.strip()!='':
    sys.path.append(app_root)
    os.chdir(app_root)

from config import *
variant = web.config.vars

web.config.debug = False
loadConfig('../cfg/debug.yaml' if web.config.debug else '/approot/cfg/config.yaml')

# import sub modules
from modules import r27api, r27db

def sig_handler(signum, frame):
    raise SystemExit()

def main():
    urls = []
    urls.extend([
        '/api',         r27api.app_api,
        '/(.+).html',   'CtrlViewController',
        '/.*',          'CtrlStaticFiles',
    ])
    app = web.application(urls, globals(), autoreload=web.config.debug)
    return app


class CtrlViewController(object):
    def GET(self, fname):
        render = variant.get_render(fname)
        if render:
            return render()
        else:
            return web.notfound()

def get_modulestaticfile(inpath):
    # get static files
    blacklist = ['./','../']
    for x in blacklist:
        if inpath.find(x)>=0:
            print('Load Static File - Illegal path: %s'%inpath)
            return ''
    contentTypes1 = {'.js':'application/javascript', '.css':'text/css', '.json':'', '.md':'', '.mdown':''}
    contentTypes2 = {'.jpg':'image/jpeg', '.jpeg':'image/jpeg', '.png':'image/png', '.gif':'image/gif', '.eot':'', '.svg':'', '.woff':'application/x-font-woff', '.woff2':'application/x-font-woff', '.ttf':'', '.otf':''}
    extName = os.path.splitext(inpath)[1].lower()
    if extName not in (list(contentTypes1.keys()) + list(contentTypes2.keys())):
        print('Load Static File - Illegal file: %s'%inpath)
        return ''
    if extName in contentTypes1.keys():
        fpath = os.path.join('../www', inpath[1:])
        ctype = contentTypes1.get(extName, "application/octet-stream; charset=UTF-8")
    elif extName in contentTypes2.keys():
        fpath = os.path.join('../www', inpath[1:])
        ctype = contentTypes2.get(extName, "application/octet-stream; charset=UTF-8")
    if not os.path.exists(fpath):
        print('Load Static File - Not exist file: %s'%fpath)
        raise web.notfound()
    try:
        f = open(fpath, 'rb')
    except IOError:
        raise web.notfound()
    web.header("Content-Type", ctype if ctype else "application/octet-stream; charset=UTF-8")
    fs = os.fstat(f.fileno())
    web.header("Content-Length", str(fs[6]))
    content = f.read()
    f.close()
    return content

class CtrlStaticFiles(object):
    def GET(self):
        return get_modulestaticfile(web.ctx.path)


if __name__ == '__main__':
    r27db.initDBConnection()
    signal.signal(signal.SIGTERM, sig_handler)
    app = main()
    if sys.argv and sys.argv[0]=='/approot/server/main.wsgi':
        # Running in Docker Container, [spawn-fcgi -f /approot/server/main.wsgi -p 9080 -u nobody -F 8 -n]
        # sys.argv[0] is /approot/server/main.wsgi
        web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
        app.run()
    elif sys.argv and sys.argv[0]=='server/main.wsgi':
        # Running in Docker Container, [python server/main.wsgi 8080]
        app.run()
    else:
        # [python main.wsgi 9000], sys.argv[0] is main.wsgi
        _thread.start_new_thread(app.run,())
        console.embed()
    print('Bye.')
