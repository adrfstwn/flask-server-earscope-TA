import cv2
import numpy as np
import base64

class EarScopeModel:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def process_image(self, image_data):
        try:
            # Decode Base64 ke gambar NumPy array
            image_bytes = base64.b64decode(image_data.split(',')[1])
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Ubah ukuran gambar untuk mempercepat pemrosesan
            img = cv2.resize(img, (640, 480))

            # Konversi ke grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Deteksi wajah dengan parameter lebih ringan
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=3, minSize=(30, 30)
            )

            # Gambar bounding box
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Encode hasil kembali ke Base64
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 70])  # Kompresi JPEG
            processed_image_base64 = base64.b64encode(buffer).decode('utf-8')
            return f"data:image/jpeg;base64,{processed_image_base64}"
        except Exception as e:
            print(f"Error processing image: {e}")
            return None