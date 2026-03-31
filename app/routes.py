from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize

main = Blueprint("main", __name__)

spectra_data = {}
min_max_norm_data = {}
z_score_norm_data = {}

@main.route("/")
def home():
    return render_template("index.html",
                           spectra_data=spectra_data,
                           min_max_norm_data=min_max_norm_data,
                           z_score_norm_data=z_score_norm_data)

@main.route("/upload_csv", methods=["POST"])
def upload_csv():
    files = request.files.getlist("files")

    for file in files:
        if file and file.filename != "":
            name = file.filename.removesuffix('.csv')
            raw_data = parse_csv(file)
            spectra_data[name] = raw_data
            min_max_norm_data[name] = min_max_normalize(raw_data)
            z_score_norm_data[name] = z_score_normalize(raw_data)

    return redirect(url_for("main.home"))

@main.route("/delete_spectra/<filename>", methods=["POST"])
def delete_spectra(filename):
    spectra_data.pop(filename, None)
    min_max_norm_data.pop(filename, None)
    z_score_norm_data.pop(filename, None)

    return redirect(url_for("main.home"))