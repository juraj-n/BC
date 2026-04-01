from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize, calculate_pearson
from .store import data

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html",
                           spectra_data=data.spectra_data,
                           min_max_norm_data=data.min_max_norm_data,
                           z_score_norm_data=data.z_score_norm_data,
                           result=data.result)

@main.route("/compare_samples", methods=["POST"])
def compare_samples():
    selected_samples = request.form.getlist("selected")
    if len(selected_samples) == 0:
        return redirect(url_for("main.home"))

    name_a = selected_samples[0]
    name_b = selected_samples[1]

    coeff = calculate_pearson(data.min_max_norm_data[name_a]["y"],
                              data.min_max_norm_data[name_b]["y"])

    data.result = [{
        "sample_a": name_a,
        "sample_b": name_b,
        "coefficient": round(coeff, 4)
    }]

    return redirect(url_for("main.home"))

@main.route("/upload_csv", methods=["POST"])
def upload_csv():
    for file in request.files.getlist("files"):
        if not file or not file.filename.lower().endswith(".csv"):
            continue

        name = file.filename.removesuffix(".csv")
        raw_data = parse_csv(file)
        data.add(name, raw_data, min_max_normalize(raw_data), z_score_normalize(raw_data))

    return redirect(url_for("main.home"))

@main.route("/delete_spectra/<filename>", methods=["POST"])
def delete_spectra(filename):
    data.delete(filename)

    return redirect(url_for("main.home"))