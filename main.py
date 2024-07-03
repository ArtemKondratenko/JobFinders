from flask import Flask
from src.database import db, create_tables

from src.views.main_page import api as main_page_api
from src.views.company import api as company_api
from src.views.employee import api as employee_api
from src.views.resume import api as resume_api
from src.views.vacancy_response import api as vacancy_response_api
from src.views.vacancy_invitations import api as vacancy_invitations_api
from src.views.vacancy import api as vacancy_api


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testdb"
app.secret_key = "h3uNFUANxnnxjzgnKAOF399"

app.register_blueprint(main_page_api)
app.register_blueprint(company_api)
app.register_blueprint(employee_api)
app.register_blueprint(resume_api)
app.register_blueprint(vacancy_api)
app.register_blueprint(vacancy_response_api)
app.register_blueprint(vacancy_invitations_api)

db.init_app(app)
create_tables(app)

if __name__ == '__main__':
  app.run(host="0.0.0.0")
