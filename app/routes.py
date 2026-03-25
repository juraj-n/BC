from flask import Blueprint, render_template, request
from .utils import parse_csv

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

@main.route("/upload", methods=["POST"])
def upload():
    return render_template("index.html")