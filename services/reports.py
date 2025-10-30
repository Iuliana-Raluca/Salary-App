import os
import pandas as pd
from datetime import date
from decimal import Decimal
from models.base import SessionLocal
from models.entities import Employee
from sqlalchemy.orm import joinedload


def _month_anchor_from_string(month_str: str) -> date:
    y, m = map(int, month_str.split("-"))
    return date(y, m, 1)


def generate_manager_csv(manager_id: int, month_str: str) -> str:
    month_anchor = _month_anchor_from_string(month_str)
    with SessionLocal() as db:
        employees = db.query(Employee).options(
            joinedload(Employee.contracts),
            joinedload(Employee.bonuses),
            joinedload(Employee.attendances)
        ).filter(Employee.manager_id == manager_id).all()

        rows = []

        for emp in employees:
            contract = next((
                c for c in emp.contracts
                if c.valid_from <= month_anchor and (not c.valid_to or c.valid_to >= month_anchor)
            ), None)
            base_salary = Decimal(contract.base_salary_monthly) if contract else Decimal("0")

            bonus_sum = sum(
                b.amount for b in emp.bonuses if b.month == month_anchor
            ) if emp.bonuses else Decimal("0")

            attendance = next((
                a for a in emp.attendances if a.month == month_anchor
            ), None)

            working_days = attendance.working_days if attendance else None
            vacation_days = attendance.vacation_days if attendance else None

            rows.append({
                "Employee": f"{emp.first_name} {emp.last_name}",
                "Base Salary": float(base_salary),
                "Bonus": float(bonus_sum),
                "Salary to Pay": float(base_salary + bonus_sum),
                "Working Days": working_days,
                "Vacation Days": vacation_days,
            })

        df = pd.DataFrame(rows)
        filename = f"report_manager_{manager_id}_{month_str}.csv"
        path = os.path.join("storage/out", filename)
        os.makedirs("storage/out", exist_ok=True)
        df.to_csv(path, index=False)

        return path
