#!/usr/bin/env python
import os
from bottle import Bottle, run, request, response, redirect, request, abort
from bottle import mako_view as view

from ninfo import Ninfo

import bottle
template_dir = os.path.join(os.path.dirname(__file__), "templates")
print 'template_dir', template_dir
bottle.TEMPLATE_PATH.insert(0, template_dir)

from decorator import decorator
@decorator
def auth(fn, *a, **kw):
    if request.environ.get('repoze.who.identity') == None:
        abort(401)
    return fn(*a, **kw)

#bottle.debug(True)
app = Bottle()

import logging
log = logging.getLogger("ninfo-web")

import threading
local_data = threading.local()

def get_info_object():
    if hasattr(local_data, 'info'):
        return local_data.info

    info = Ninfo()
    log.debug("Creating new info object for %s" % threading.currentThread())
    local_data.info = info
    return info

@app.route("/info/text/:plugin/:arg")
@auth
def info_text(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    response.content_type = "text/plain"
    return P.get_info_text(plugin, arg)

@app.route("/info/html/:plugin/:arg")
@auth
def info_html(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    return P.get_info_html(plugin, arg)

@app.route("/info/json/:plugin/:arg")
@auth
def info_json(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    return P.get_info_json(plugin, arg)

@app.route("/")
@app.route("/info")
@auth
@view("info.mako")
def info():
    P = get_info_object()
    arg = request.GET.get("arg",'')
    plugins = []
    if arg:
        all_plugins = P.plugin_classes
        relevant_plugins = [p for p in all_plugins if P.compatible_argument(p.name, arg)]
        plugins = sorted(relevant_plugins, key=lambda x:x.name)
    return {"arg": arg, "plugins": plugins}

@app.route("/aboutplugin/:plugin")
@view("aboutplugin.mako")
def aboutplugin(plugin):
    P = get_info_object()
    p = P.get_plugin(plugin)
    return {"p": p}


import make_auth
app = make_auth.make_auth_app(app)

def main():
    logging.basicConfig(level=logging.DEBUG)
    run(app, server='auto', port=8000)

if __name__ == "__main__":
    main()
