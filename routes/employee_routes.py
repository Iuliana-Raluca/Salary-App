from flask import Blueprint, request, jsonify
from config import Config
from services.employees import *

bp = Blueprint("employees", __name__)

def _auth_ok():
    return request.headers.get("X-API-KEY") == Config.MANAGER_API_KEY

@bp.post("/employees")
def create_employee_route():
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    payload = request.get_json()
    emp = create_employee(payload)
    if not emp:
        return jsonify({"error": "manager not found"}), 404
    return jsonify({
        "id": emp.id,
        "name": f"{emp.first_name} {emp.last_name}",
        "email": emp.email,
        "manager_id": emp.manager_id
    }), 201

@bp.get("/employees")
def list_employees_route():
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    emps = list_employees()
    return jsonify([
        {
            "id": e.id,
            "name": f"{e.first_name} {e.last_name}",
            "email": e.email,
            "manager_id": e.manager_id
        } for e in emps
    ])

@bp.get("/employees/<int:eid>")
def get_employee_route(eid):
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    e = get_employee(eid)
    if not e:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": e.id,
        "first_name": e.first_name,
        "last_name": e.last_name,
        "email": e.email,
        "active": e.active,
        "manager_id": e.manager_id
    })

@bp.patch("/employees/<int:eid>")
def update_employee_route(eid):
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    e = update_employee(eid, data)
    if not e:
        return jsonify({"error": "not found"}), 404
    return jsonify({
        "id": e.id,
        "name": f"{e.first_name} {e.last_name}"
    })

@bp.delete("/employees/<int:eid>")
def delete_employee_route(eid):
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    ok = delete_employee(eid)
    return jsonify({"deleted": ok})
