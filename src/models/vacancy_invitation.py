from __future__ import annotations

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db
import typing

if typing.TYPE_CHECKING:
  from src.models.resume import Resume
  from src.models.vacancy import Vacancy


class VacancyInvitation(db.Model, MappedAsDataclass):
  id: Mapped[int] = mapped_column(primary_key=True, init=False)
  resume_id: Mapped[int] = mapped_column(ForeignKey("resume.id"))
  resume: Mapped[Resume] = relationship("Resume",
                                        back_populates="vacancy_invitations",
                                        init=False)
  vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancy.id"))
  vacancy: Mapped[Vacancy] = relationship("Vacancy",
                                          back_populates="vacancy_invitations",
                                          init=False)

  @staticmethod
  def get(vacancy_id: int, resume_id: int):
    return db.session.scalars(select(VacancyInvitation).where(
      VacancyInvitation.vacancy_id == vacancy_id, VacancyInvitation.resume_id == resume_id)).first()

  def save(self):
    db.session.add(self)
    db.session.commit()
