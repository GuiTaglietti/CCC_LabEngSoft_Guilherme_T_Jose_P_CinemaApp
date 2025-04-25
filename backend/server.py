from flask import Flask, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import psycopg2
from config import Config
from psycopg2.extras import RealDictCursor

# Estabelece a conexão com o banco de dados e cria um cursor
def get_db():
    """Estabelece a conexão com o banco de dados e cria um cursor"""
    if not hasattr(g, 'db'):  # Se o objeto g não tiver o banco, cria a conexão
        g.db = psycopg2.connect(
            dbname=Config.DATABASE_NAME,
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD,
            host=Config.DATABASE_HOST,
            port=Config.DATABASE_PORT
        )
        g.cursor = g.db.cursor(cursor_factory=RealDictCursor)  # Para retornar como dicionário
    return g.cursor

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    jwt = JWTManager(app)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
