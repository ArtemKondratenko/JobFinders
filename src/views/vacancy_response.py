from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db

api = Blueprint('vacancy_resp_api', __name__)


@api.post("/vacancy_responses")
def create_vacancy_response():
  vacancy_id = int(request.form["vacancy_id"])
  resume_id = int(request.form["resume_id"])

  employee = auth.get_current_employee()
  if not employee:
    abort(401)

  resume = Resume.get(resume_id)
  if not resume:
    abort(404)

  if resume.employee != employee:
    abort(401)
  if VacancyResponse.get(vacancy_id, resume_id):
    abort(409)

  vacancy_response = VacancyResponse(vacancy_id=vacancy_id,
                                     resume_id=resume_id)
  try:
    vacancy_response.save()
    return redirect("/vacancies")
  except Exception:
    return "Ошибка при создании ответа"


@api.get("/responses")
def viewing_page_responses():
  company = auth.get_current_company()
  if not company:
    abort(401)
  vacancy_responses = Vacancy.all_responses_company(company)
  return render_template("company_vacancy_response.html",
                         vacancy_responses=vacancy_responses)
