from flask import Blueprint, request, jsonify
from config import Config
from services.reports import generate_manager_csv

bp = Blueprint("reports", __name__)

@bp.post("/createAggregatedEmployeeData")
def create_csv():
    if request.headers.get("X-API-KEY") != Config.MANAGER_API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json() or {}
    manager_id = int(payload.get("manager_id", 0))
    month = payload.get("month") 

    if not manager_id or not month:
        return jsonify({"error": "Missing manager_id or month"}), 400

    csv_path = generate_manager_csv(manager_id, month)
    return jsonify({"status": "ok", "csv": csv_path})
