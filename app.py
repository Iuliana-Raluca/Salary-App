from flask import Flask
from config import Config
from models.base import Base, engine
from routes.manager_routes import bp as manager_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Base.metadata.create_all(bind=engine)

    app.register_blueprint(manager_bp)

    @app.get("/health")
    def health():
        return {"ok": True}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)

