from flask import Blueprint, render_template, request
from .utils import parse_csv

main = Blueprint("main", __name__)

uploaded_file = []

@main.route("/")
def home():
    return render_template("layout.html", files=uploaded_file)

@main.route("/upload", methods=["POST"])
def upload():
    global uploaded_file
    files = request.files.getlist("files")

    for file in files:
        uploaded_file.append(file.filename)
    
    return render_template("layout.html", files=uploaded_file)