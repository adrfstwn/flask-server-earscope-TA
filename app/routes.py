from flask import Blueprint, jsonify, render_template
from .database import test_db_connection
from flask import Blueprint, jsonify
from flask_socketio import emit
from .detector import process_frame_with_model



bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@bp.route('/test-db', methods=['GET'])
def test_db():
    result = test_db_connection()
    if isinstance(result, dict):
        return jsonify(result), 500
    return jsonify({"message": result}), 200

# Fungsi untuk menangani event WebSocket
def handle_process_frame(data):
    try:
        image_data = data.get('image')
        if not image_data:
            emit('processed_frame', {'error': 'No image data provided'})
            return

        print("Processing frame...")  # Debugging log
        processed_image = process_frame_with_model(image_data)
        print("Sending processed frame back to frontend")  # Debugging log

        emit('processed_frame', {'processed_image': processed_image})
    except Exception as e:
        print(f"Error processing frame: {e}")  # Debugging log
        emit('processed_frame', {'error': str(e)})

# Registrasi event WebSocket
def register_socketio_events(socketio):
    @socketio.on('process_frame')
    def process_frame_event(data):
        print("Received frame from frontend")  # Debugging log
        handle_process_frame(data)