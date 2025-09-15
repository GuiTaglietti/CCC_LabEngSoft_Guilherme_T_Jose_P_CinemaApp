from flask import Flask, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import psycopg2
from config import Config
from psycopg2.extras import RealDictCursor

def get_db():
    if not hasattr(g, 'db'):
        g.db = psycopg2.connect(
            dbname=Config.DATABASE_NAME,
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD,
            host=Config.DATABASE_HOST,
            port=Config.DATABASE_PORT
        )
        g.cursor = g.db.cursor(cursor_factory=RealDictCursor)
    return g.cursor

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    jwt = JWTManager(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.routes.movies import movies_bp
    app.register_blueprint(movies_bp, url_prefix='/api/movies')

    from app.routes.sessions import sessions_bp
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')

    from app.routes.maintenance import maintenance_bp
    app.register_blueprint(maintenance_bp, url_prefix='/api/maintenance/messages')

    from app.routes.tickets import tickets_bp
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
