from flask import Blueprint, redirect, render_template, request, abort

api = Blueprint('main_api', __name__)


@api.get("/")
def home():
    return redirect("/pages/main_page")


@api.get("/pages/main_page")
def get_login_page():
    return render_template("main_page.html")
