from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, ForeignKey, Numeric, UniqueConstraint
from .base import Base
from datetime import date
from decimal import Decimal

class Manager(Base):
    __tablename__ = "managers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True)

    employees: Mapped[list["Employee"]] = relationship(back_populates="manager")


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    cnp: Mapped[str] = mapped_column(String(32), unique=True)
    hire_date: Mapped[date]
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    manager_id: Mapped[int] = mapped_column(ForeignKey("managers.id"))
    manager: Mapped["Manager"] = relationship(back_populates="employees")
    contracts: Mapped[list["SalaryContract"]] = relationship(back_populates="employee")
    bonuses: Mapped[list["Bonus"]] = relationship(back_populates="employee")
    attendances: Mapped[list["Attendance"]] = relationship(back_populates="employee")


class SalaryContract(Base):
    __tablename__ = "salary_contracts"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    base_salary_monthly: Mapped[float] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8), default="RON")
    valid_from: Mapped[date]
    valid_to: Mapped[date | None] = mapped_column(nullable=True)

    employee: Mapped["Employee"] = relationship(back_populates="contracts")

class Bonus(Base):
    __tablename__ = "bonuses"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    month: Mapped[date] = mapped_column() 
    description: Mapped[str] = mapped_column(String(255))
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    currency: Mapped[str] = mapped_column(String(8), default="RON")

    employee: Mapped["Employee"] = relationship(back_populates="bonuses")


class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))
    month: Mapped[date] = mapped_column() 
    working_days: Mapped[int]
    vacation_days: Mapped[int]

    employee: Mapped["Employee"] = relationship(back_populates="attendances")

    __table_args__ = (
        UniqueConstraint("employee_id", "month", name="uq_attendance_emp_month"),
    )