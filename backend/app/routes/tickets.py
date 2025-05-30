from flask import Blueprint, request, jsonify
from server import get_db
from datetime import datetime

tickets_bp = Blueprint('tickets', __name__, url_prefix='/api/tickets')

@tickets_bp.route('/seats/<int:session_id>', methods=['GET'])
def get_seats(session_id):
    cursor = get_db()
    cursor.execute("SELECT id, seat_number, is_occupied FROM seats WHERE session_id = %s", (session_id,))
    seats = cursor.fetchall()
    return jsonify(seats), 200

@tickets_bp.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    seat_id = data.get('seat_id')
    payment_method = data.get('payment_method')
    payment_id = data.get('payment_id')

    cursor = get_db()
    cursor.execute("UPDATE seats SET is_occupied = TRUE WHERE id = %s", (seat_id,))

    cursor.execute("""
        INSERT INTO tickets (user_id, session_id, seat_id, payment_status, payment_method, payment_id)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
    """, (user_id, session_id, seat_id, 'paid', payment_method, payment_id))

    ticket_id = cursor.fetchone()['id']
    cursor.connection.commit()

    return jsonify({'ticket_id': ticket_id, 'msg': 'Ingresso criado com sucesso!'}), 201

@tickets_bp.route('/tickets/<int:user_id>', methods=['GET'])
def get_user_tickets(user_id):
    cursor = get_db()
    cursor.execute("""
        SELECT t.id, t.payment_status, t.purchase_time, s.seat_number, se.start_time, se.end_time, m.title
        FROM tickets t
        JOIN seats s ON t.seat_id = s.id
        JOIN sessions se ON t.session_id = se.id
        JOIN movies m ON se.movie_id = m.id
        WHERE t.user_id = %s
    """, (user_id,))
    
    tickets = cursor.fetchall()
    return jsonify(tickets), 200

@tickets_bp.route('/all', methods=['GET'])
def get_all_tickets():
    cursor = get_db()
    cursor.execute("""
        SELECT t.id, t.payment_status, t.purchase_time, s.seat_number, se.start_time, se.end_time, m.title
        FROM tickets t
        JOIN seats s ON t.seat_id = s.id
        JOIN sessions se ON t.session_id = se.id
        JOIN movies m ON se.movie_id = m.id
    """)
    tickets = cursor.fetchall()
    return jsonify(tickets), 200

@tickets_bp.route('/total', methods=['GET'])
def get_tickets_count():
    cursor = get_db()
    cursor.execute("""
        SELECT COUNT(*) AS total FROM tickets
    """)
    total = cursor.fetchone()
    return jsonify({'total': total['total']}), 200