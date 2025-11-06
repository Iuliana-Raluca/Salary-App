from flask import Flask, request
from config import Config
from models.base import Base, engine
from routes.manager_routes import bp as manager_bp
from routes.employee_routes import bp as employee_bp
from routes.contract_routes import bp as contract_bp
from routes.report_routes import bp as reports_bp
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Base.metadata.create_all(bind=engine)

    app.register_blueprint(manager_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(contract_bp)
    app.register_blueprint(reports_bp)

    @app.get("/health")
    def health():
        return {"ok": True}

    os.makedirs("logs", exist_ok=True)

    log_file = os.path.join("logs", "app.log")
    file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def log_request():
        app.logger.info(f"{request.method} {request.path} from {request.remote_addr}")

    @app.after_request
    def log_response(response):
        app.logger.info(f"Response: {response.status_code} for {request.path}")
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)
