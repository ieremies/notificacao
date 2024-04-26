#!/usr/bin/env python3
from flask import Flask, request, render_template, send_file
from parser import parse
from writer import writer

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        writer(parse(text)).save()
        return send_file("overlay.pdf", as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
