from typing import Optional, List
from models.base import SessionLocal
from models.entities import Manager

def create_manager(name: str, email: str) -> Manager:
    with SessionLocal() as db:
        m = Manager(name=name, email=email)
        db.add(m)
        db.commit()
        db.refresh(m)
        return m

def get_manager(mid: int) -> Optional[Manager]:
    with SessionLocal() as db:
        return db.get(Manager, mid)

def list_managers() -> List[Manager]:
    with SessionLocal() as db:
        return db.query(Manager).order_by(Manager.id).all()

def update_manager(mid: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[Manager]:
    with SessionLocal() as db:
        m = db.get(Manager, mid)
        if not m:
            return None
        if name is not None:
            m.name = name
        if email is not None:
            m.email = email
        db.commit()
        db.refresh(m)
        return m

def delete_manager(mid: int) -> bool:
    with SessionLocal() as db:
        m = db.get(Manager, mid)
        if not m:
            return False
        db.delete(m)
        db.commit()
        return True
