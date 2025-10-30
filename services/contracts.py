from datetime import date
from models.base import SessionLocal
from models.entities import SalaryContract, Employee

def get_active_contract(employee_id: int, month: date) -> SalaryContract | None:
    with SessionLocal() as db:
        return db.query(SalaryContract).filter(
            SalaryContract.employee_id == employee_id,
            SalaryContract.valid_from <= month,
            (SalaryContract.valid_to == None) | (SalaryContract.valid_to >= month)
        ).first()
