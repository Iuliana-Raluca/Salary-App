from flask import Blueprint, request, jsonify
from datetime import date
from models.base import SessionLocal
from models.entities import SalaryContract

bp = Blueprint("contracts", __name__)

@bp.post("/contracts")
def create_contract():
    data = request.get_json()
    with SessionLocal() as db:
        c = SalaryContract(
            employee_id=data["employee_id"],
            base_salary_monthly=data["base_salary"],
            currency=data.get("currency", "RON"),
            valid_from=date.fromisoformat(data["valid_from"]),
            valid_to=date.fromisoformat(data["valid_to"]) if data.get("valid_to") else None
        )
        db.add(c)
        db.commit()
        db.refresh(c)
        return jsonify({
            "id": c.id,
            "employee_id": c.employee_id,
            "base_salary": str(c.base_salary_monthly),
            "valid_from": c.valid_from.isoformat()
        }), 201
