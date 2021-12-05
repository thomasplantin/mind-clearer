from flask import Flask, session, abort, render_template, redirect, flash, request, jsonify
# from flask_pymongo import PyMongo
from pymongo import MongoClient
from pip._vendor import cachecontrol
from env import config
from datetime import datetime, date
from functools import wraps
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
import requests
import google
import os
import json

template_dir = os.path.abspath("public/templates")
static_dir = os.path.abspath("public/static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = config.APP_SECRET

# MongoDB setup
cluster = MongoClient(config.MONGO_CONNECTION_STRING)
db = cluster[config.MONGO_DB]
users_collection = db[config.MONGO_USERS_COLLECTION]
thoughts_collection = db[config.MONGO_THOUGHTS_COLLECTION]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

client_secrets_file = os.path.join(
    os.path.abspath("env"), "client_secret.json")

with open("./env/client_secret.json", "r") as file:
    client_secrets = json.load(file)

GOOGLE_CLIENT_ID = client_secrets["web"]["client_id"]
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
            ],
    redirect_uri="http://127.0.0.1:{}/callback".format(config.PORT)
)


# Define decorator
def login_required(function):
    # Renaming wrapper with the function name to avoid overwritting existing endpoint function
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "_id" not in session:
            flash("You need to login first")
            return abort(401)  # Return HTTP status code "401 - Unauthorized"
        else:
            return function(*args, **kwargs)
    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    if not users_collection.count_documents({"_id": id_info.get('sub')}):
        new_user = {
            "_id": id_info.get('sub'),
            "first_name": id_info.get('given_name'),
            "last_name": id_info.get('family_name'),
            "full_name": id_info.get('name'),
            "email": id_info.get('email'),
            "date_joined": datetime.now(),
            "picture_url": id_info.get('picture')
        }
        users_collection.insert_one(new_user)
    else:
        print("User already exists.")

    session["_id"] = id_info.get('sub')
    session["full_name"] = id_info.get('name')
    session["first_name"] = id_info.get('given_name')
    session["last_name"] = id_info.get('family_name')
    session["email"] = id_info.get('email')
    session["picture_url"] = id_info.get('picture')
    return redirect("/home")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/features")
def features():
    return render_template("features.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/home")
@login_required
def protected_area():
    today = date.today().strftime("%B %d, %Y")
    return render_template("home.html", user=session["first_name"], date=today)


@app.route("/thoughts")
@login_required
def get_thoughts():
    return render_template("thoughts.html",  user=session["first_name"])


@app.route("/profile")
@login_required
def get_profile():
    return render_template("profile.html",  user=session["full_name"], picture_url=session["picture_url"], email=session["email"])


@app.route("/delete-profile")
@login_required
def delete_profile():
    users_collection.delete_one({"_id": session["_id"]})
    thoughts_collection.delete_many({"_id": session["_id"]})
    session.clear()
    return render_template("index.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=config.PORT)
