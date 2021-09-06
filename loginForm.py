import os
import pathlib

import cachecontrol as cachecontrol
import google.auth.transport.requests
from flask import Flask, abort, session, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

loginForm = Flask("Google Login App")
loginForm.secret_key = "NA"

GOOGLE_CLIENT_ID ="441614906312-di2a4sf0cd71f5l0tt36ak4b9iips5t8.apps.googleusercontent.com"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent,"client_secret_google.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#change new from here //
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper


@loginForm.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session[state] = state
    return redirect(authorization_url)


    #return redirect("/protected_area")


@loginForm.route("/callback")
def callback():
    flow.fetch_token(authorization_respose=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)
    credentials = flow.credentials
    request_session = request.session()
    cache_session = cachecontrol.Cachecontrol(request_session)
    token_session = google.auth.transport.requests.request(session = cache_session)

    id_info_gg = id_token.verify_oauth2_token(id_token= credentials._id_token, request=token_session, audience= GOOGLE_CLIENT_ID)
    return id_info_gg



@loginForm.route("/logout")
def logout():
    session.clear()
    return redirect("/index_pointer")

@loginForm.route("/")
def index_pointer():
    return "Hello World" "<a href='/login'><button> Login </button> </a>"

@loginForm.route(("/protected_area"))
#@login_required
def protected_area():
    return "Protected""<a href='/logout'><button> Logout </button> </a>"


if __name__ == '__main__':
    loginForm.run(debug=True)
