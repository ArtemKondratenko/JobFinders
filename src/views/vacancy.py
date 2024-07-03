from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db
api = Blueprint('vacancy_api', __name__)

@api.post("/vacancies")
def create_vacancy():
  name = request.form["name"]
  description = request.form["description"]
  company = auth.get_current_company()
  if not company:
    abort(403)
  vacancy = Vacancy(name=name, description=description, company_id=company.id)
  try:
    vacancy.save()
    return redirect("/pages/home_company")
  except Exception:
    return "Ошибка при создании вакансии"


@api.get("/vacancies")
def viewing_page_vacancies():
  vacancies = Vacancy.get_opened()
  employee = auth.get_current_employee()
  return render_template("vacancies.html",
                         vacancies=vacancies,
                         employee=employee)