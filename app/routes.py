from flask import Blueprint, render_template
from app.detector import process_frame_with_model, start_recording, stop_recording

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

# Fungsi untuk menangani event WebSocket
def handle_process_frame(data):
    from app import socketio  # Tambahkan ini agar `emit` berfungsi
    from flask_socketio import emit
    try:
        image_data = data.get('image')
        if not image_data:
            socketio.emit('processed_frame', {'error': 'No image data provided'})  # <--- Gunakan `socketio.emit`
            return
        print("Processing frame...")  # Debugging log
        processed_image = process_frame_with_model(image_data)
        print("Sending processed frame back to frontend")  # Debugging log
        socketio.emit('processed_frame', {'processed_image': processed_image})  # <--- Gunakan `socketio.emit`
    except Exception as e:
        print(f"Error processing frame: {e}")  # Debugging log
        socketio.emit('processed_frame', {'error': str(e)})  # <--- Gunakan `socketio.emit`

# Registrasi event WebSocket
def register_socketio_events(socketio):
    @socketio.on('process_frame')
    def process_frame_event(data):
        print("Received frame from frontend")  # Debugging log
        handle_process_frame(data)

    @socketio.on('start_recording')
    def handle_start_recording():
        print("Starting recording...")
        start_recording()

    @socketio.on('stop_recording')
    def handle_stop_recording():
        print("Stopping recording...")
        stop_recording()
