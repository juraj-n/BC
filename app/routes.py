from flask import Blueprint, render_template, request
from .utils import parse_csv

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/spectra", methods=["POST"])
def spectra():
    file = request.files.get("file")
    if not file:
        return "No file uploaded", 400
    
    try:
        data = parse_csv(file)
    except ValueError as e:
        return str(e), 400
    
    return render_template("spectra.html", data=data)