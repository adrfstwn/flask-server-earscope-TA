from earscope_model.earscope_model import EarScopeModel
import base64
import numpy as np
import cv2

import queue
from threading import Thread
import time

# Inisialisasi model (hanya sekali)
model = EarScopeModel()

# Queue untuk frame yang akan diproses
frame_queue = queue.Queue(maxsize=10)  # Batasi kapasitas queue agar tidak overload

def process_frame_with_model(image_data):
    """
    Fungsi untuk memproses frame menggunakan model.
    :param image_data: Gambar dalam format Base64.
    :return: Gambar hasil proses dalam format Base64.
    """
    try:
        # Decode Base64 ke gambar NumPy array
        image_bytes = base64.b64decode(image_data.split(',')[1])
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Proses dengan model
        processed_img = model.process_image(img)
        # Encode hasil kembali ke Base64 untuk dikirim ke frontend
        _, buffer = cv2.imencode('.jpg', processed_img, [cv2.IMWRITE_JPEG_QUALITY, 70])
        processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{processed_image_base64}"
    except Exception as e:
        print(f"Error processing frame: {e}")
        return None

def process_frames():
    while True:
        if not frame_queue.empty():
            try:
                # Ambil frame dari queue
                image_data = frame_queue.get()
                
                # Proses frame menggunakan model
                processed_image_base64 = process_frame_with_model(image_data)
                
                # Kirim hasil ke frontend melalui WebSocket
                from app import socketio  # Pastikan socketio sudah diinisialisasi
                socketio.emit('processed_frame', {'processed_image': processed_image_base64})
                
                # Tandai bahwa item di queue sudah selesai diproses
                frame_queue.task_done()
            except Exception as e:
                print(f"Error processing frame in thread: {e}")
        else:
            time.sleep(0.01)  # Jeda jika tidak ada frame
            
# Inisialisasi thread untuk pemrosesan frame
processing_thread = Thread(target=process_frames, daemon=True)
processing_thread.start()

def start_recording():
    """Memulai perekaman video"""
    model.start_recording()

def stop_recording():
    """Menghentikan perekaman video"""
    model.stop_recording()