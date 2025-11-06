import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.pdfencrypt import StandardEncryption
from datetime import date
from decimal import Decimal
from models.entities import Employee, SalaryContract, Bonus
from config import Config
from models.base import SessionLocal
from sqlalchemy.orm import joinedload

def generate_employee_pdf(employee: Employee, month: date, out_path: str):
    contract = next((
        c for c in employee.contracts
        if c.valid_from <= month and (not c.valid_to or c.valid_to >= month)
    ), None)
    base_salary = Decimal(contract.base_salary_monthly) if contract else Decimal("0")

    # preluarea bonusurilor din luna respectiva
    bonus_sum = sum(
        b.amount for b in employee.bonuses if b.month == month
    ) if employee.bonuses else Decimal("0")

    total = base_salary + bonus_sum

    # criptarea fisierului cu parola, care reprezinta CNP ul angajatului
    encrypt = StandardEncryption(employee.cnp, ownerPassword=employee.cnp)

    c = canvas.Canvas(out_path, pagesize=A4, encrypt=encrypt)
    width, height = A4

    lines = [
        f"Fluturas salariu - {month.strftime('%B %Y')}",
        "",
        f"Nume angajat: {employee.first_name} {employee.last_name}",
        f"ID angajat: {employee.id}",
        f"CNP: {employee.cnp}",
        "",
        f"Salariu de baza: {base_salary:.2f} RON",
        f"Bonusuri: {bonus_sum:.2f} RON",
        f"Total de plata: {total:.2f} RON",
    ]

    y = height - 72
    for line in lines:
        c.drawString(72, y, line)
        y -= 20

    c.save()

def generate_pdfs_for_manager(manager_id: int, month: date) -> list[str]:
    with SessionLocal() as db:
        employees = db.query(Employee).options(
            joinedload(Employee.contracts),
            joinedload(Employee.bonuses)
        ).filter(Employee.manager_id == manager_id).all()

        output_paths = []

        for emp in employees:
            filename = f"slip_emp_{emp.id}_{month.strftime('%Y_%m')}.pdf"
            path = os.path.join(Config.STORAGE_OUT, filename)
            os.makedirs(Config.STORAGE_OUT, exist_ok=True)

            generate_employee_pdf(emp, month, path)
            output_paths.append(path)

        return output_paths