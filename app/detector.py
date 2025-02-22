from earscope_model.earscope_model import EarScopeModel
import base64
import numpy as np
import cv2

# Inisialisasi model (hanya sekali)
model = EarScopeModel()

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

def start_recording():
    """Memulai perekaman video"""
    model.start_recording()

def stop_recording():
    """Menghentikan perekaman video"""
    model.stop_recording()