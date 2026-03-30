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
            name = file.filename.removesuffix('.csv')
            spectra_data[name] = parse_csv(file)

    return redirect(url_for("main.home"))

@main.route("/delete_spectra/<filename>", methods=["POST"])
def delete_spectra(filename):
    spectra_data.pop(filename, None)

    return redirect(url_for("main.home"))