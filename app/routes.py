from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize, l1_normalize
from .utils import calculate_matrix, pearson_coeff, cosine_similarity, euclidean_distance, spectral_angle_mapper
from .store import ComparisonData, data

main = Blueprint("main", __name__)

@main.route("/")
def home():
    raw     = {name: data.spectra[name].raw for name in data.comparison.samples} if data.comparison else {}
    min_max = {name: data.spectra[name].min_max for name in data.comparison.samples} if data.comparison else {}
    z_score = {name: data.spectra[name].z_score for name in data.comparison.samples} if data.comparison else {}
    l1      = {name: data.spectra[name].l1 for name in data.comparison.samples} if data.comparison else {}

    return render_template("base.html",
                           spectra=data.spectra,
                           comparison=data.comparison,
                           raw_selected=raw,
                           min_max_selected=min_max,
                           z_score_selected=z_score,
                           l1_selected = l1
                           )

@main.route("/run_analysis", methods=["POST"])
def run_analysis():
    selected_names = request.form.getlist("selected")
    if len(selected_names) < 2:
        return redirect(url_for("main.home"))
    
    comparison = ComparisonData()
    comparison.samples = selected_names

    comparison.metrics["pearson"] = calculate_matrix(data.spectra, selected_names, pearson_coeff)
    comparison.metrics["euclidean"] = calculate_matrix(data.spectra, selected_names, euclidean_distance)
    comparison.metrics["cosine"] = calculate_matrix(data.spectra, selected_names, cosine_similarity)
    comparison.metrics["sam"] = calculate_matrix(data.spectra, selected_names, spectral_angle_mapper)

    data.comparison = comparison

    return redirect(url_for("main.home"))

@main.route("/upload_csv", methods=["POST"])
def upload_csv():
    for file in request.files.getlist("files"):
        if not file or not file.filename.lower().endswith(".csv"):
            continue

        name = file.filename.removesuffix(".csv")
        raw_data = parse_csv(file)
        data.add(name, raw_data, min_max_normalize(raw_data), z_score_normalize(raw_data), l1_normalize(raw_data))

    return redirect(url_for("main.home"))

@main.route("/delete_spectra/<spectrum_name>", methods=["POST"])
def delete_spectra(spectrum_name):
    data.delete(spectrum_name)

    return redirect(url_for("main.home"))