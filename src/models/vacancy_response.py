from __future__ import annotations
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db
import typing



if typing.TYPE_CHECKING:
  from src.models.vacancy import Vacancy
  from src.models.resume import Resume


class VacancyResponse(db.Model, MappedAsDataclass):
  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"))
  vacancy: Mapped[Vacancy] = relationship("Vacancy",
                                          back_populates="responses",
                                          init=False)
  resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id"))
  resume: Mapped[Resume] = relationship("Resume",
                                        back_populates="responses",
                                        init=False)

  def save(self):
   db.session.add(self)
   db.session.commit()


  @staticmethod
  def get(vacancy_id: int, resume_id: int):
    return db.session.scalars(select(VacancyResponse).where(
      VacancyResponse.vacancy_id == vacancy_id, VacancyResponse.resume_id == resume_id)).first()
