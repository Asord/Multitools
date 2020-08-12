from flask import render_template
from Libraries.AsemcoAPI.Tools.Services import registerView, Views

def index():
    return render_template("index.html", views=Views)

registerView(index, "/", desc="index")