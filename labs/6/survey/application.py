import csv

from flask import Flask, jsonify, redirect, render_template, request
from flask_session import Session

# Configure application
app = Flask(__name__)

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():

    # Validate submission
    for field in ["name", "house", "position"]:
        value = request.form.get(field)
        if not value:
            return render_template("error.html", message=f"You must specify your {field}.")

    # Write submission to CSV
    with open("survey.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow((request.form.get("name"),
                         request.form.get("house"),
                         request.form.get("position")))

    # Redirect to /sheet
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return render_template("sheet.html", rows=rows)
