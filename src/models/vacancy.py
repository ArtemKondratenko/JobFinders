from __future__ import annotations
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db
import typing

if typing.TYPE_CHECKING:
    from src.models.vacancy_response import VacancyResponse
    from src.models.vacancy_invitation import VacancyInvitation
    from src.models.company import Company


class Vacancy(db.Model, MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    description: Mapped[str]
    company_id: Mapped[int] = mapped_column(ForeignKey("company.id"))
    company: Mapped[Company] = relationship("Company",
                                            back_populates="vacancies",
                                            init=False)
    responses: Mapped[list[VacancyResponse]] = relationship(
        "VacancyResponse", back_populates="vacancy", init=False)
    opened: Mapped[bool] = mapped_column(default=True)
    vacancy_invitations: Mapped[list[VacancyInvitation]] = relationship(
        "VacancyInvitation", back_populates="vacancy", init=False)

    @staticmethod
    def get_opened() -> Iterable[Vacancy]:
        vacancies = db.session.scalars(
            select(Vacancy).where(Vacancy.opened == True)).all()
        return vacancies

    @staticmethod
    def all_responses_company(company: Company) -> Iterable[VacancyResponse]:
        from src.models.vacancy_response import VacancyResponse
        return db.session.scalars(
            select(VacancyResponse).join(Vacancy).where(
                Vacancy.company_id == company.id)).all()

    def save(self):
        db.session.add(self)
        db.session.commit()



