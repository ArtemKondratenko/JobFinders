from flask import Blueprint, redirect, render_template, request, abort
from src import auth
from src.models import Employee, Company, Resume, Vacancy, VacancyResponse, VacancyInvitation
from src.database import db
api = Blueprint('vacanci_invi_api', __name__)

@api.post("/invitation_interview")
def create_vacancy_invitation():
  vacancy_id = int(request.form["vacancy_id"])
  resume_id = int(request.form["resume_id"])
  company = auth.get_current_company()
  if not company:
    abort(401)
  resume = Resume.get(resume_id)
  if not resume:
    abort(404)
  if Company.vacancy_belongs_company(vacancy_id) != company:
    abort(401)
  if VacancyInvitation.get(vacancy_id, resume_id):
    abort(409)
  vacancy_invitation = VacancyInvitation(vacancy_id=vacancy_id, resume_id=resume_id)
  try:
    vacancy_invitation.save()
    return redirect("/resumies")
  except Exception:
    return "Ошибка при создании приглашения на собеседование"