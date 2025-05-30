from flask import Blueprint, request, jsonify
from datetime import datetime
from server import get_db

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')


@sessions_bp.route('/', methods=['GET'])
def get_all_sessions():
    cursor = get_db()
    cursor.execute("""
        SELECT s.*, m.title AS movie_title
        FROM sessions s
        JOIN movies m ON s.movie_id = m.id
        ORDER BY s.start_time
    """)
    sessions = cursor.fetchall()
    return jsonify([dict(session) for session in sessions]), 200


@sessions_bp.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):
    cursor = get_db()
    cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    session = cursor.fetchone()
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404
    return jsonify(dict(session)), 200


@sessions_bp.route('/', methods=['POST'])
def create_session():
    data = request.json
    cursor = get_db()

    cursor.execute("SELECT * FROM movies WHERE id = %s", (data['movie_id'],))
    movie = cursor.fetchone()
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404

    cursor.execute("""
        SELECT * FROM sessions
        WHERE room = %s
        AND (%s <= end_time AND %s >= start_time)
    """, (
        data['room'],
        data['end_time'],
        data['start_time']
    ))
    conflict = cursor.fetchone()
    if conflict:
        return jsonify({"error": "Já existe uma sessão nessa sala nesse horário"}), 400

    cursor.execute("""
        INSERT INTO sessions (movie_id, room, start_time, end_time)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (
        data['movie_id'],
        data['room'],
        data['start_time'],
        data['end_time']
    ))

    session_id = cursor.fetchone()['id']

    seats = []
    for row in ['A', 'B']:
        for num in range(1, 11):
            seat_number = f"{row}{num}"
            seats.append((session_id, seat_number))

    cursor.executemany(
        "INSERT INTO seats (session_id, seat_number) VALUES (%s, %s)",
        seats
    )

    cursor.connection.commit()

    return jsonify({
        "message": "Sessão criada com sucesso e 20 assentos adicionados!",
        "session_id": session_id
    }), 201




@sessions_bp.route('/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    data = request.json
    cursor = get_db()

    cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    session = cursor.fetchone()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    cursor.execute("""
        SELECT * FROM sessions
        WHERE room = %s
        AND id != %s
        AND (%s < end_time AND %s > start_time)
    """, (
        data['room'],
        session_id,
        data['end_time'],
        data['start_time']
    ))
    conflict = cursor.fetchone()
    if conflict:
        return jsonify({"error": "Time conflict in the selected room"}), 400

    cursor.execute("""
        UPDATE sessions
        SET movie_id = %s, room = %s, start_time = %s, end_time = %s, updated_at = %s
        WHERE id = %s
    """, (
        data['movie_id'],
        data['room'],
        data['start_time'],
        data['end_time'],
        datetime.utcnow(),
        session_id
    ))
    cursor.connection.commit()
    return jsonify({"message": "Session updated"}), 200



@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    cursor = get_db()
    cursor.execute("SELECT * FROM sessions WHERE id = %s", (session_id,))
    session = cursor.fetchone()
    if not session:
        return jsonify({"error": "Session not found"}), 404

    cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
    cursor.connection.commit()
    return jsonify({"message": "Session deleted"}), 200
