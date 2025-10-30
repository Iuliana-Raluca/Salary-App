from flask import Flask
from config import Config
from models.base import Base, engine
from routes.manager_routes import bp as manager_bp
from routes.employee_routes import bp as employee_bp
from routes.contract_routes import bp as contract_bp
from routes.report_routes import bp as reports_bp


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

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)

