from __future__ import annotations

from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from typing import Iterable
from src.database import db
import typing

if typing.TYPE_CHECKING:
    from src.models.resume import Resume
    from src.models.vacancy_invitation import VacancyInvitation


class Employee(db.Model, MappedAsDataclass):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    resumes: Mapped[list[Resume]] = relationship(init=False)

    @staticmethod
    def get_employee_by_email_with_password_check(
            email: str, password: str) -> Employee | None:
        employee = db.session.scalars(
            select(Employee).where(Employee.email == email,
                                   Employee.password == password)).first()
        return employee

    @staticmethod
    def get(id: int):
        return db.session.query(Employee).get(id)

    @property
    def vacancy_invitations(self) -> Iterable[VacancyInvitation]:
        from src.models.employee import Employee
        from src.models.resume import Resume
        from src.models.vacancy_invitation import VacancyInvitation

        vacancy_invitation = db.session.scalars(
            select(VacancyInvitation).join(Resume).where(Resume.employee_id == Employee.id)).all()

        return vacancy_invitation

    def save(self):
        db.session.add(self)
        db.session.commit()
