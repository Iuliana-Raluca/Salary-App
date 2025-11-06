from flask import Blueprint, request, jsonify
from config import Config
from services.reports import generate_manager_csv
from services.pdf_generator import generate_pdfs_for_manager
from services.archive import archive_files 
from datetime import date
from services.emailer import send_email_with_attachments
from services.archive import archive_files
from services.reports import generate_manager_csv
from models.base import SessionLocal
from models.entities import Manager, Employee



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

@bp.post("/createPdfForEmployees")
def create_pdfs():
    if request.headers.get("X-API-KEY") != Config.MANAGER_API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json() or {}
    manager_id = int(payload.get("manager_id", 0))
    month_str = payload.get("month") 

    if not manager_id or not month_str:
        return jsonify({"error": "Missing data"}), 400

    y, m = map(int, month_str.split("-"))
    month = date(y, m, 1)

    pdfs = generate_pdfs_for_manager(manager_id, month)
    label = f"pdfs_manager_{manager_id}_{month.strftime('%Y_%m')}"
    zip_path = archive_files(pdfs, label)

    return jsonify({
        "status": "ok",
        "pdf_files": pdfs,
        "zip" : zip_path
    })

@bp.post("/sendAggregatedEmployeeData")
def send_csv():
    if request.headers.get("X-API-KEY") != Config.MANAGER_API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json() or {}
    manager_id = int(payload.get("manager_id", 0))
    month_str = payload.get("month")

    if not manager_id or not month_str:
        return jsonify({"error": "Missing manager_id or month"}), 400

    csv_path = generate_manager_csv(manager_id, month_str)

    with SessionLocal() as db:
        m = db.get(Manager, manager_id)
        if not m:
            return jsonify({"error": "Manager not found"}), 404

    send_email_with_attachments(
        to=m.email,
        subject=f"Salary report for {month_str}",
        body="Attached you can find the aggregated salary report for your employees.",
        attachments=[csv_path]
    )

    zip_path = archive_files([csv_path], f"csv_manager_{manager_id}_{month_str.replace('-', '_')}")

    return jsonify({
        "status": "sent",
        "csv": csv_path,
        "zip": zip_path
    })

@bp.post("/sendPdfToEmployees")
def send_pdfs():
    if request.headers.get("X-API-KEY") != Config.MANAGER_API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    payload = request.get_json() or {}
    manager_id = int(payload.get("manager_id", 0))
    month_str = payload.get("month")

    if not manager_id or not month_str:
        return jsonify({"error": "Missing manager_id or month"}), 400

    y, m = map(int, month_str.split("-"))
    month = date(y, m, 1)

    pdf_paths = generate_pdfs_for_manager(manager_id, month)

    sent = []

    with SessionLocal() as db:
        employees = db.query(Employee).filter(Employee.manager_id == manager_id).all()
        by_id = {e.id: e for e in employees}

        for path in pdf_paths:
            try:
                emp_id = int(path.split("slip_emp_")[1].split("_")[0])
            except Exception:
                continue

            emp = by_id.get(emp_id)
            if emp:
                send_email_with_attachments(
                    to=emp.email,
                    subject=f"Fluturas salariu {month.strftime('%Y-%m')}",
                    body="Pentru a deschide fisierul PDF va rugam sa folositi CNP-ul ca si parola.s",
                    attachments=[path]
                )
                sent.append({
                    "employee_id": emp.id,
                    "email": emp.email,
                    "pdf": path
                })

    label = f"pdfs_manager_{manager_id}_{month.strftime('%Y_%m')}"
    zip_path = archive_files(pdf_paths, label)

    return jsonify({
        "status": "sent",
        "sent_count": len(sent),
        "pdf_sent": sent,
        "zip": zip_path
    })
