from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import os


from flask import Flask, request, render_template, send_from_directory, jsonify
import os

from DistantRepresentatives import LInf, LOne
from DistantRepresentativesRectangles import DistantRepresentativesRectangles

import json
from ast import literal_eval

def create_app():
    app = Flask(__name__)

    @app.route("/listening", methods=("POST","GET"))
    def computeReps():

        if request.method == "POST" or request.method == "GET":
            
            rects = literal_eval(request.json["rects"])
            dr = DistantRepresentativesRectangles(LOne)
            delta, p = dr.getDistantRepresentatives(rects)

            return {"p": p, "delta": delta }


    @app.route("/getting/<name>", methods=("GET",))
    def getReps(name):
        rects = literal_eval(name)
        dr = DistantRepresentativesRectangles(LOne)
        delta, p = dr.getDistantRepresentatives(rects)

        return {"p": p, "delta": delta }


    @app.route('/', methods=('GET',))
    def register():
        return render_template("distantreps.html")

    return app

app = create_app()