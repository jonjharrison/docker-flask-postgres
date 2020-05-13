import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for,
    render_template
)
#from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate

from project.models.shared import db
from project.models.users import User

app = Flask(__name__)
app.config.from_object("project.config.Config")
db.init_app(app)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return jsonify(hello="world")


@app.route("/users/")
def users():
    data = {
        "users": db.session.query(User)
    }
    return render_template("users.html", data=data)


@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
