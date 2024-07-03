from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db

api = Blueprint('employee_api', __name__)


@api.get("/pages/create_employee")
def get_register_employee_page():
    return render_template("create_employee.html")


@api.post("/employees")
def register_employee():
    name = request.form["name"]
    password = request.form["password"]
    email = request.form["email"]
    employee = Employee(name=name, password=password, email=email)
    try:
        employee.save()
        auth.login_employee(employee)
        return redirect("/pages/home_employee")
    except Exception:
        return "Ошибка при регистрации"


@api.get("/pages/home_employee")
def home_page_employee():
    employee = auth.get_current_employee()
    if not employee:
        return redirect("/pages/login")
    return render_template("home_employee.html", employee=employee)


@api.get("/pages/login_employee")
def get_login_employee():
    return render_template("login_employee.html")


@api.post("/authorization_employee")
def login_employee():
    email = request.form["email"]
    password = request.form["password"]
    employee = Employee.get_employee_by_email_with_password_check(
        email, password)
    if not employee:
        return redirect("/pages/create_employee")
    auth.login_employee(employee)
    return render_template("home_employee.html", employee=employee)


@api.get("/logout")
def logout():
    auth.logout()
    return redirect("/pages/login_employee")


@api.get("/view_job_offers")
def view_job_offers():
    employee = auth.get_current_employee()
    if not employee:
        return redirect("/pages/create_employee")
    return render_template("view_job_offers.html", vacancy_invitations=employee.vacancy_invitations)
