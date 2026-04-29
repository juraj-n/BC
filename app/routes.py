from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv, min_max_normalize, z_score_normalize, l1_normalize, create_residual, zones_coeffs
from .utils import calculate_matrix, pearson_coeff, spectral_angle_mapper
from .store import data

main = Blueprint("main", __name__)

@main.context_processor
def inject_sidebar_data():
    return dict(spectra=data.spectra)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/run_analysis", methods=["POST"])
def run_analysis():
    selected_names = request.form.getlist("selected")
    
    if len(selected_names) < 2:
        return redirect(url_for("main.home"))
    
    if len(selected_names) == 2:
        return redirect(url_for("main.detail_analysis", selected=selected_names))
    
    return redirect(url_for("main.multi_analysis", selected=selected_names))

@main.route("/multi_analysis", methods=["GET"])
def multi_analysis():
    selected_names = request.args.getlist("selected")

    raw     = {name: data.spectra[name].raw     for name in selected_names}
    z_score = {name: data.spectra[name].z_score for name in selected_names}
    l1      = {name: data.spectra[name].l1      for name in selected_names}
    min_max = {name: data.spectra[name].min_max for name in selected_names}

    pearson = calculate_matrix(data.spectra, selected_names, pearson_coeff)
    sam     = calculate_matrix(data.spectra, selected_names, spectral_angle_mapper)

    return render_template("analysis.html",
                           samples=selected_names,
                           raw=raw, z_score=z_score, l1=l1, min_max=min_max,
                           pearson=pearson, sam=sam)

@main.route("/detail_analysis", methods=["GET"])
def detail_analysis():
    selected_names = request.args.getlist("selected")

    raw     = {name: data.spectra[name].raw     for name in selected_names}
    z_score = {name: data.spectra[name].z_score for name in selected_names}
    l1      = {name: data.spectra[name].l1      for name in selected_names}
    min_max = {name: data.spectra[name].min_max for name in selected_names}

    name_a, name_b = selected_names[0], selected_names[1]
    residual = create_residual(l1, name_a, name_b)

    zone_metrics = zones_coeffs(l1, name_a, name_b)

    return render_template("detail.html",
                           samples=selected_names,
                           raw=raw, z_score=z_score, l1=l1, min_max=min_max,
                           residual=residual,
                           zone_metrics=zone_metrics)

@main.route("/upload_file", methods=["POST"])
def upload_file():
    for file in request.files.getlist("files"):
        if not file or not file.filename.lower().endswith(".csv"):
            continue
        
        name = file.filename.removesuffix(".csv")
        raw_data = parse_csv(file)
        
        if raw_data is not None: 
            data.add(name,
                     raw_data,
                     min_max_normalize(raw_data),
                     z_score_normalize(raw_data),
                     l1_normalize(raw_data)
                     )

    return redirect(url_for("main.home"))

@main.route("/delete_spectra/<spectrum_name>", methods=["POST"])
def delete_spectra(spectrum_name):
    data.delete(spectrum_name)

    return redirect(url_for("main.home"))