from flask import session
from src.models import Employee, Company


def login_employee(employee: Employee):
  session["employee"] = employee.id

def login_company(company: Company):
  session["company"] = company.id

def logout():
  # session.pop("employee")
  # session.pop("company")
  session.clear()

def get_current_employee() -> Employee | None:
  employee_id = session.get("employee")
  if not employee_id:
    return None
  return Employee.get(employee_id)

def get_current_company() -> Company | None:
  company_id = session.get("company")
  if not company_id:
    return None
  return Company.get(company_id)


