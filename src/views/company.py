from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db

api = Blueprint('company_api', __name__)


@api.get("/pages/create_company")
def get_register_company_page():
  return render_template("create_company.html")


@api.post("/companies")
def register_company():
  name = request.form["name"]
  password = request.form["password"]
  email = request.form["email"]
  company = Company(name=name, password=password, email=email)
  try:
    company.save()
    auth.login_company(company)
    return redirect("/pages/home_company")
  except Exception:
    return "Ошибка при регистрации"


@api.get("/pages/home_company")
def home_page_company():
  company = auth.get_current_company()
  if not company:
    return redirect("/pages/create_company")
  return render_template("home_company.html", company=company)


@api.get("/pages/login_company")
def get_login_company():
  return render_template("login_company.html")


@api.post("/authorization_company")
def login_company():
  email = request.form["email"]
  password = request.form["password"]
  company = Company.get_company_by_email_with_password_check(
      email, password)
  if not company:
    return "Компания с таким email'ом и/или паролем не найдена"
  auth.login_company(company)
  return redirect("/pages/home_company")

@api.get("/logout")
def logout():
  auth.logout()
  return redirect("/pages/login_company")









