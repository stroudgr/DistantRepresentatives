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

        if request.method == "POST":
            #print("Received post")

            
            rects = literal_eval(request.json["rects"])

            dr = DistantRepresentativesRectangles(LOne)
            delta, p = dr.getDistantRepresentatives(rects)

            return {"p": p, "delta": delta }

        if request.method == "GET":
            #response = jsonify(message="Simple server is running")

            # Enable Access-Control-Allow-Origin
            #response.headers.add("Access-Control-Allow-Origin", "*")

            return "###"#response
    
    from . import auth
    app.register_blueprint(auth.bp)

    from . import draw
    app.register_blueprint(draw.bp)

    
    @app.route('/another', methods=('GET', 'POST'))
    def register():

        if request.method == "POST":
            return "1acd"


        return render_template("distantreps.html")

    @app.route('/blank')
    def blank():
        return "1234"

    return app


  #  """