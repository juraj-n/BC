from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv

main = Blueprint("main", __name__)

spectra_data = {}

@main.route("/")
def home():
    return render_template("index.html", spectra_data=spectra_data)

@main.route("/upload_csv", methods=["POST"])
def upload_csv():
    files = request.files.getlist("files")

    for file in files:
        if file and file.filename != "":
            spectra_data[file.filename] = parse_csv(file)

    return redirect(url_for("main.home"))