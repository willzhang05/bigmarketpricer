#!/usr/bin/python3
import sys
import os
from flask import Flask, redirect, session, url_for, render_template, request, send_from_directory
from urllib.parse import urlparse, urljoin, urlencode

CLIENT_ID = "omNihUKDY7L8XXLh41WTTY9Pda21T2SRqAmJO86C"
CLIENT_SECRET = "fmdfCpUwDIu0E5FExHudOdySDSa7HPhNrRKTirNsXJIWc2NEMFJtiY7UaczcTJL2kzRnsBV4OWPQ8P8KTv8YDqS5rdOOAE0opdYBLbZtMzNTfnCWHTJTgmpmDDtSbjDY"
REDIRECT_URI = "https://dev.wzhang.me/login"

AUTH_BASE_URL = "https://ion.tjhsst.edu/oauth/authorize/"
TOKEN_URL = "https://ion.tjhsst.edu/oauth/token/"

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
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
    '''nexturl = request.args.get("next")
    if not is_safe_url(nexturl):
        return flask.abort(400)'''
    return render_template("index.html")

'''
@app.route("/hours/")
def hours():
    if "oauth_token" in session:
        profile_json = session.get("profile")

        hours = Hour.query.filter_by(name=profile_json['full_name'])
        return render_template("hours.html", hours=hours)

    return redirect(url_for("login", next="hours"))


@app.route("/admin/")
def admin():
    if "oauth_token" in session:
        #profile_json = session.get("profile", {})
        username = session.get("username", {})
        admins = ["2018wzhang", "2018nzhou"]
        if username in admins:
            announcements = Announcement.query.all()
            hours = Hour.query.all()
            return render_template(
                "admin.html",
                announcements=announcements,
                hours=hours)
        return "Unauthorized"

    return redirect(url_for("login", next="admin"))


@app.route("/login/", methods=["get"])
def login():
    nexturl = request.args.get("next")
    if not is_safe_url(nexturl):
        return flask.abort(400)

    oauth = OAuth2Session(
        CLIENT_ID, redirect_uri=REDIRECT_URI, scope=["read"])
    if "code" not in request.args:
        authorization_url, state = oauth.authorization_url(AUTH_BASE_URL)
        session["next"] = nexturl
        return redirect(authorization_url)
    try:
        token = oauth.fetch_token(
            TOKEN_URL, code=request.args.get(
                "code", ""), client_secret=CLIENT_SECRET)
        profile = oauth.get("https://ion.tjhsst.edu/api/profile")
        profile_data = json.loads(profile.content.decode())
        session["profile"] = profile_data
        session["username"] = profile_data["ion_username"]
        session["oauth_token"] = token
        return redirect(url_for(session["next"]))
    except InvalidGrantError:
        return redirect(url_for("login"))
'''

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
