from flask import Blueprint, request, jsonify
from config import Config
from services.managers import (
    create_manager, get_manager, list_managers, update_manager, delete_manager
)

bp = Blueprint("managers", __name__)

def _auth_ok():
    return request.headers.get("X-API-KEY") == Config.MANAGER_API_KEY

@bp.post("/managers")
def create_manager_route():
    if not _auth_ok():
        return jsonify({"error": "unauthorized"}), 401
    payload = request.get_json() or {}
    name = payload.get("name")
    email = payload.get("email")
    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400
    m = create_manager(name=name, email=email)
    return jsonify({"id": m.id, "name": m.name, "email": m.email}), 201