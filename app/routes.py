from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize, calculate_pearson_matrix, calculate_euclidean_dist_matrix, calculate_cosine_similarity_matrix
from .store import ComparisonData, data

main = Blueprint("main", __name__)

@main.route("/")
def home():
    raw     = {name: data.spectra[name].raw for name in data.comparison.samples} if data.comparison else {}
    min_max = {name: data.spectra[name].min_max for name in data.comparison.samples} if data.comparison else {}
    z_score = {name: data.spectra[name].z_score for name in data.comparison.samples} if data.comparison else {}

    return render_template("index.html",
                           spectra=data.spectra,
                           comparison=data.comparison,
                           raw_selected=raw,
                           min_max_selected=min_max,
                           z_score_selected=z_score
                           )

@main.route("/run_analysis", methods=["POST"])
def run_analysis():
    selected_names = request.form.getlist("selected")
    if len(selected_names) < 2:
        return redirect(url_for("main.home"))
    
    comparison = ComparisonData()
    comparison.samples = selected_names

    comparison.metrics["pearson"] = calculate_pearson_matrix(data.spectra, selected_names)
    comparison.metrics["euclidean"] = calculate_euclidean_dist_matrix(data.spectra, selected_names)
    comparison.metrics["cosine"] = calculate_cosine_similarity_matrix(data.spectra, selected_names)

    data.comparison = comparison

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

@main.route("/delete_spectra/<spectrum_name>", methods=["POST"])
def delete_spectra(spectrum_name):
    data.delete(spectrum_name)

    return redirect(url_for("main.home"))