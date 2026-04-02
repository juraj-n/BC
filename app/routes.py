from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize, calculate_pearson
from .store import data

main = Blueprint("main", __name__)

@main.route("/")
def home():
    raw     = {name: v["raw"]     for name, v in data.selected_samples.items()}
    min_max = {name: v["min_max"] for name, v in data.selected_samples.items()}
    z_score = {name: v["z_score"] for name, v in data.selected_samples.items()}

    return render_template("index.html",
                           spectra_data=data.spectra_data,
                           comparison_matrix=data.comparison_matrix,
                           raw_selected=raw,
                           min_max_selected=min_max,
                           z_score_selected=z_score
                           )

@main.route("/compare_samples", methods=["POST"])
def compare_samples():
    selected_samples = request.form.getlist("selected")
    if len(selected_samples) < 2:
        return redirect(url_for("main.home"))
    
    data.selected_samples = {
        name: {
            "raw": data.spectra_data[name],
            "min_max": data.min_max_norm_data[name],
            "z_score": data.z_score_norm_data[name]
        }
        for name in selected_samples if name in data.spectra_data
    }

    matrix = []
    for name_a in selected_samples:
        row = []
        for name_b in selected_samples:
            coeff = calculate_pearson(data.min_max_norm_data[name_a]["y"],
                                      data.min_max_norm_data[name_b]["y"])
            row.append(round(coeff, 3))
        matrix.append(row)

    data.comparison_matrix = {
        "samples": selected_samples,
        "matrix": matrix
    }

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