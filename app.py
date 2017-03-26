#!/usr/bin/python3
import sys
import os
import subprocess
import ebay_price
from flask import Flask, redirect, session, url_for, render_template, request, send_from_directory
from urllib.parse import urlparse, urljoin, urlencode

os.environ["FLASK_DEBUG"]="1"
app = Flask(__name__)

import json

# print(os.environ["APP_SETTINGS"])


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.values.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


def redirect_back(endpoint, **values):
    target = request.form["next"]
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/search/", methods=["POST"])
def search():
    data = request.form
    if any(data) and data["terms"] != "":
        info = ebay_price.get_price(data["terms"], data["category"])
        proc = subprocess.check_call(["node", "/var/www/bigmarketpricer/wrangler.js", data["terms"], data["category"], data["price"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        listings = json.loads(proc.stdout)
        print(listings)
        #listings = json.load(open("./test.json"))
        return render_template("results.html", info=info, listings=listings)
    else:
        return redirect(url_for("index"))

@app.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("static/css", path)


@app.route("/scripts/<path:path>")
def send_js(path):
    return send_from_directory("static/scripts", path)


@app.route("/icons/<path:path>")
def send_icons(path):
    return send_from_directory("static/icons", path)


@app.route("/images/<path:path>")
def send_images(path):
    return send_from_directory("static/images", path)


@app.route("/fonts/<path:path>")
def send_fonts(path):
    return send_from_directory("static/fonts", path)

'''
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("index"))
'''


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Please specify a port")
        exit()
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
