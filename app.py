import logging
import os
import pathlib

import requests

import cachecontrol as cachecontrol
import google.auth.transport.requests
from flask import Flask , abort , session , redirect , request , render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow







app = Flask("Google Login App")
app.secret_key = "NA"

GOOGLE_CLIENT_ID = "441614906312-di2a4sf0cd71f5l0tt36ak4b9iips5t8.apps.googleusercontent.com"

client_secrets_file = os.path.join(pathlib.Path(__file__).parent , "client_secret_google.json")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# change new from here //
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file ,
    scopes=["https://www.googleapis.com/auth/userinfo.profile" , "https://www.googleapis.com/auth/userinfo.email" ,
            "openid"] ,
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_required(function) :
    def wrapper(*args , **kwargs) :
        if "google_id" not in session :
            return abort(401)
        else :
            return function()

    return wrapper


@app.route("/login")
def login() :
    authorization_url , state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

    # return redirect("/protected_area")


@app.route("/callback")
def callback() :
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"] :
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token ,
        request=token_request ,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout() :
    session.clear()
    return redirect("/")


@app.route("/")
def index_pointer() :
    return "Hello World" "<a href='/login'><button> Login </button> </a>"


@app.route(("/protected_area"))
# @login_required
def protected_area() :
    return render_template('InputGoogle.html' , name=f"Hello {session['name']}!")


if __name__ == '__main__' :
    app.run(debug=True)
