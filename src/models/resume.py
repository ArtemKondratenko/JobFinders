from __future__ import annotations

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db

import typing


if typing.TYPE_CHECKING:
  from src.models.employee import Employee
  from src.models.vacancy_response import VacancyResponse
  from src.models.vacancy_invitation import VacancyInvitation


class Resume(db.Model, MappedAsDataclass):
  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  name: Mapped[str]
  description: Mapped[str]
  employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
  employee: Mapped[Employee] = relationship(
      "Employee", back_populates="resumes", lazy="joined", init=False
  )  #связанные объекты Employee загружаются автоматически при доступе к свойству employee объекта Resume
  responses: Mapped[list[VacancyResponse]] = relationship(
      "VacancyResponse", back_populates="resume", init=False)
  vacancy_invitations: Mapped[list[VacancyInvitation]] = relationship(
      "VacancyInvitation", back_populates="resume", init=False)
  opened: Mapped[bool] = mapped_column(default=True)

  @staticmethod
  def get(id: int):
    return db.session.query(Resume).get(id)

  @staticmethod
  def get_opened() -> Iterable[Resume]:
    resumies = db.session.scalars(
        select(Resume).where(Resume.opened == True)).all()
    return list(resumies)

  def save(self):
   db.session.add(self)
   db.session.commit()
