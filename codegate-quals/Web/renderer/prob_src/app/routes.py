from flask import Flask, render_template, render_template_string, request, redirect, abort, Blueprint
import urllib2
import time
import hashlib

from os import path
from urlparse import urlparse

front = Blueprint("renderer", __name__)

@front.before_request
def test():
    print(request.url)

@front.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    
    url = request.form.get("url")
    res = proxy_read(url) if url else False
    if not res:
        abort(400)

    return render_template("index.html", data = res)

@front.route("/whatismyip", methods=["GET"])
def ipcheck():
    return render_template("ip.html", ip = get_ip(), real_ip = get_real_ip())

@front.route("/admin", methods=["GET"])
def admin_access():
    ip = get_ip()
    rip = get_real_ip()

    if ip not in ["127.0.0.1", "127.0.0.2"]: #super private ip :)
        abort(403)

    if ip != rip: #if use proxy
        ticket = write_log(rip)
        return render_template("admin_remote.html", ticket = ticket)

    else:
        if ip == "127.0.0.2" and request.args.get("body"):
            ticket = write_extend_log(rip, request.args.get("body"))
            return render_template("admin_local.html", ticket = ticket)
        else:
            return render_template("admin_local.html", ticket = None)

@front.route("/admin/ticket", methods=["GET"])
def admin_ticket():
    ip = get_ip()
    rip = get_real_ip()

    if ip != rip: #proxy doesn't allow to show ticket
        print 1
        abort(403)
    if ip not in ["127.0.0.1", "127.0.0.2"]: #only local
        print 2
        abort(403)
    if request.headers.get("User-Agent") != "AdminBrowser/1.337":
        print request.headers.get("User-Agent")
        abort(403)
    
    if request.args.get("ticket"):
        log = read_log(request.args.get("ticket"))
        if not log:
            print 4
            abort(403)
        return render_template_string(log)

def get_ip():
    return request.remote_addr

def get_real_ip():
    return request.headers.get("X-Forwarded-For") or get_ip()

def proxy_read(url):
    #TODO : implement logging
    
    s = urlparse(url).scheme
    if s not in ["http", "https"]: #sjgdmfRk akfRk
        return ""

    return urllib2.urlopen(url).read()

def write_log(rip):
    tid = hashlib.sha1(str(time.time()) + rip).hexdigest()
    with open("/home/tickets/%s" % tid, "w") as f:
        log_str = "Admin page accessed from %s" % rip
        f.write(log_str)
    
    return tid

def write_extend_log(rip, body):
    tid = hashlib.sha1(str(time.time()) + rip).hexdigest()
    with open("/home/tickets/%s" % tid, "w") as f:
        f.write(body)

    return tid

def read_log(ticket):
    if not (ticket and ticket.isalnum()):
        return False
    
    if path.exists("/home/tickets/%s" % ticket):
        with open("/home/tickets/%s" % ticket, "r") as f:
            return f.read()
    else:
        return False
