from app import app
import flask
from flask import Flask, render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/major_key.html')
def major_key():
    # return render_template('index.html')
    return "major"


@app.route('/minor_key.html')
def minor_key():
    return "minor"


@app.route('/increase_volume.html')
def increase_volume():
    return "increasevolume"


@app.route('/decrease_volume.html')
def decrease_volume():
    return "decreasevolume"


@app.route('/increase_tempo.html')
def increase_tempo():
    return "increasetempo"


@app.route('/decrease_tempo.html')
def decrease_tempo():
    return "decreasetempo"


@app.route("/add_bassline.html")
def add_baseline():
    return "bassline"


@app.route('/add_harmony.html')
def add_harmony():
    return "harmony"


@app.route('/change_instrument.html')
def change_instrument():
    return "instrument"


if __name__ = "__main__":
    app.run(host='165.227.188.38')