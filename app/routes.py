from flask import Blueprint, render_template, request, redirect, url_for
from .utils import parse_csv

main = Blueprint("main", __name__)

uploaded_file_names = []
x = []
y = []

@main.route("/")
def home():
    return render_template("index.html", file_names=uploaded_file_names, x=x, y=y)

@main.route("/spectra", methods=["POST"])
def spectra():
    files = request.files.getlist("files")

    global uploaded_file_names
    global x
    global y
    for file in files:
        if file and file.filename != "":
            uploaded_file_names.append(file.filename)
            data = parse_csv(file)
            x = [point[0] for point in data]
            y = [point[1] for point in data]

    return redirect(url_for("main.home"))