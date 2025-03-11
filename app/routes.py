import os
from flask import Blueprint, render_template, send_from_directory, current_app
from app.detector import process_frame_with_model, start_recording, stop_recording

bp = Blueprint('main', __name__)

@bp.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js')

@bp.route('/manifest.json')
def manifest():
    return send_from_directory(os.path.dirname(current_app.root_path), 'manifest.json')

@bp.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

# Fungsi untuk menangani event WebSocket
def handle_process_frame(data):
    from app import socketio 
    try:
        image_data = data.get('image')
        if not image_data:
            socketio.emit('processed_frame', {'error': 'No image data provided'})
            return
        
        print("Processing frame...")  # Debug log
        processed_image = process_frame_with_model(image_data)  # Proses gambar

        if processed_image:
            print("Sending processed frame back to frontend")  # Debug log
            socketio.emit('processed_frame', {'processed_image': processed_image})  # Kirim segera ke frontend
        else:
            print("Failed to process frame.")  # Debug log
            socketio.emit('processed_frame', {'error': 'Frame processing failed'})

    except Exception as e:
        print(f"Error processing frame: {e}")
        socketio.emit('processed_frame', {'error': str(e)})


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
