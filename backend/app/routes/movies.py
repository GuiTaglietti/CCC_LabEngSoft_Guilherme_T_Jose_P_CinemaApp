from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from server import get_db
from datetime import datetime
import os

movies_bp = Blueprint('movies', __name__, url_prefix='/api/movies')

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@movies_bp.route('/', methods=['GET'])
def get_all_movies():
    cursor = get_db()
    cursor.execute("SELECT * FROM movies ORDER BY release_date DESC")
    movies = cursor.fetchall()
    movies = [dict(movie) for movie in movies]
    return jsonify(movies), 200

@movies_bp.route('/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    cursor = get_db()
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    if movie:
        return jsonify(dict(movie)), 200
    return jsonify({"error": "Movie not found"}), 404

@movies_bp.route('/', methods=['POST'])
def create_movie():
    data = request.json
    cursor = get_db()
    cursor.execute("""
        INSERT INTO movies (title, duration, genre, description, banner_url, release_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['title'],
        data['duration'],
        data['genre'],
        data.get('description', ''),
        data.get('banner_url', ''),
        data['release_date']
    ))
    cursor.connection.commit()
    return jsonify({"message": "Movie created"}), 201

@movies_bp.route('/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    data = request.json
    cursor = get_db()

    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    cursor.execute("""
        UPDATE movies
        SET title = %s, duration = %s, genre = %s, description = %s,
            banner_url = %s, release_date = %s, updated_at = %s
        WHERE id = %s
    """, (
        data['title'],
        data['duration'],
        data['genre'],
        data.get('description', ''),
        data.get('banner_url', ''),
        data['release_date'],
        datetime.utcnow(),
        movie_id
    ))
    cursor.connection.commit()
    return jsonify({"message": "Movie updated"}), 200

@movies_bp.route('/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    cursor = get_db()

    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    if not movie:
        return jsonify({"error": "Movie not found"}), 404

    cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
    cursor.connection.commit()
    return jsonify({"message": "Movie deleted"}), 200

@movies_bp.route('/upload', methods=['POST'])
def upload_banner():
    if 'banner' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['banner']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    banner_url = f'static/uploads/{filename}'

    return jsonify({'banner_url': banner_url}), 200
