# on utilise Flask
# ici c'est le back-end
# pour executer le fichier, faire 'python -m flask run' dans le terminal

import re
from datetime import datetime

from flask import Flask
#pour lier des fichiers au script python
from flask import render_template


app = Flask(__name__)


@app.route("/hello/")
# ce sera par exemple la page http://127.0.0.1:5000/hello/jean 
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/kanji_list_test/")
#l'objectif est de faire la liste des kanji ici
def kanji_list_test():
    return render_template("hello_there.html",
        
           
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

# Replace the existing home function with the one below
@app.route("/")
def home():
    return render_template("home.html")

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")
