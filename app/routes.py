from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv

main = Blueprint("main", __name__)

uploaded_files = []

@main.route("/")
def home():
    return render_template("index.html", files=uploaded_files)

@main.route("/spectra", methods=["POST"])
def spectra():
    files = request.files.getlist("files")

    global uploaded_files
    for file in files:
        if file and file.filename != "":
            uploaded_files.append(file)

    return redirect(url_for("main.home"))