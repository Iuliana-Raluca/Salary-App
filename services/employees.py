from models.base import SessionLocal
from models.entities import Employee, Manager
from typing import Optional, List
from datetime import date

def create_employee(data: dict) -> Optional[Employee]:
    with SessionLocal() as db:
        manager = db.get(Manager, data["manager_id"])
        if not manager:
            return None

        e = Employee(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            cnp=data["cnp"],
            hire_date=data.get("hire_date", date.today()),
            active=True,
            manager_id=manager.id
        )
        db.add(e)
        db.commit()
        db.refresh(e)
        return e

def list_employees() -> List[Employee]:
    with SessionLocal() as db:
        return db.query(Employee).order_by(Employee.id).all()

def get_employee(eid: int) -> Optional[Employee]:
    with SessionLocal() as db:
        return db.get(Employee, eid)

def update_employee(eid: int, data: dict) -> Optional[Employee]:
    with SessionLocal() as db:
        e = db.get(Employee, eid)
        if not e:
            return None
        for key in ["first_name", "last_name", "email", "active"]:
            if key in data:
                setattr(e, key, data[key])
        db.commit()
        db.refresh(e)
        return e

def delete_employee(eid: int) -> bool:
    with SessionLocal() as db:
        e = db.get(Employee, eid)
        if not e:
            return False
        db.delete(e)
        db.commit()
        return True
