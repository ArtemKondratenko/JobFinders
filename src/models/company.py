from __future__ import annotations

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db
import typing

if typing.TYPE_CHECKING:
    from src.models.vacancy import Vacancy


class Company(db.Model, MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    vacancies: Mapped[list[Vacancy]] = relationship(init=False)

    @staticmethod
    def get_company_by_email_with_password_check(
            email: str, password: str) -> Company | None:
        company = db.session.scalars(
            select(Company).where(Company.email == email,
                                  Company.password == password)).first()
        if company:
            return company
        return None

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get(id: int):
        return db.session.query(Company).get(id)

    @staticmethod
    def vacancy_belongs_company(vacancy_id: int) -> Company | None:
        from src.models.vacancy import Vacancy
        return db.session.scalars(select(Company).where(
            Company.vacancies.any(Vacancy.id == vacancy_id))).first()
