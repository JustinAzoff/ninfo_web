#!/usr/bin/env python
import os
import cgi
from bottle import Bottle, run, request, response, redirect, request, abort, json_dumps, static_file
from bottle import mako_view as view

from ninfo import Ninfo, util

import bottle
template_dir = os.path.join(os.path.dirname(__file__), "templates")
static_dir   = os.path.join(os.path.dirname(__file__), "static")
print 'template_dir', template_dir
bottle.TEMPLATE_PATH.insert(0, template_dir)

bottle.debug(True)
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


@app.route('/static/<path:path>')
def callback(path):
    return static_file(path, root=static_dir)

@app.route("/info/plugins")
def info_plugins():
    P = get_info_object()
    plugins = [p.as_json() for p in P.plugin_classes]
    return {"plugins": plugins}

@app.route("/info/text/:plugin/:arg")
def info_text(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout or 60
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    response.content_type = "text/plain"
    options = request.GET
    print options
    return P.get_info_text(plugin, arg, options)

@app.route("/info/html/:plugin/:arg")
def info_html(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout or 60
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    options = request.GET
    return P.get_info_html(plugin, arg, options)

@app.route("/info/json/:plugin/:arg")
def info_json(plugin, arg):
    P = get_info_object()
    if plugin not in P.plugins:
        abort(404)
    timeout = P.get_plugin(plugin).cache_timeout or 60
    response.headers['Cache-Control'] = 'max-age=%d' %  timeout
    options = request.GET
    return P.get_info_json(plugin, arg, options)

@app.route("/")
@app.route("/info")
@view("info.mako")
def info():
    P = get_info_object()
    query = request.GET.get("arg",'')
    arg = ""
    options = {}
    plugins = []
    if query:
        args, options = util.parse_query(query)
        arg = args[0]
        all_plugins = P.plugin_classes
        relevant_plugins = [p for p in all_plugins if P.compatible_argument(p.name, arg)]
        plugins = sorted(relevant_plugins, key=lambda x:x.name)
        options = json_dumps(options)
        query = cgi.escape(query, quote=True)
    return {"query": query, "arg": arg, "plugins": plugins, "options": options}

@app.route("/multiple")
@app.post("/multiple")
@view("multiple.mako")
def multiple():
    P = get_info_object()
    q = request.POST.get('q','')
    nodes = q.split()
    enabled_plugins = []
    if q:
        enabled_plugins = request.POST.getall("plugins")
    all_plugins = P.plugin_classes
    return {"q": q,
            "nodes": nodes,
            "plugins": all_plugins,
            "nodes_js": json_dumps(nodes),
            "plugins_js": json_dumps(enabled_plugins),
            "enabled_plugins": enabled_plugins
            }

@app.route("/aboutplugin/:plugin")
@view("aboutplugin.mako")
def aboutplugin(plugin):
    P = get_info_object()
    p = P.get_plugin(plugin)
    return {"p": p}

@app.route("/extract")
def extract():
    q = request.GET.get("q", "")
    print "q=", q
    #FIXME: use ip+mac finder code
    args = q.split()
    return {"args": args}

def main():
    logging.basicConfig(level=logging.DEBUG)
    run(app, server='auto', port=8000)

if __name__ == "__main__":
    main()
