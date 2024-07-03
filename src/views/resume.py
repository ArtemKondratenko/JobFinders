from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db
api = Blueprint('resume_api', __name__)





@api.post("/resumes")
def create_resume():
  name = request.form["name"]
  description = request.form["description"]
  employee = auth.get_current_employee()
  if not employee:
    abort(403)
  resume = Resume(name=name, description=description, employee_id=employee.id)
  try:
    resume.save()
    return redirect("/pages/home_employee")
  except Exception:
    return "Ошибка при создании вакансии"


@api.get("/resumies")
def viewing_page_resumes():
  resumies = Resume.get_opened()
  company = auth.get_current_company()
  return render_template("resumies.html",
                         resumies=resumies,
                         company=company)


