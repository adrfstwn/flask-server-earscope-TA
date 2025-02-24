import cv2
import os
from datetime import datetime
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# Buat folder video jika belum ada
output_dir = "video"
os.makedirs(output_dir, exist_ok=True)

class EarScopeModel:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Parameter video
        self.frame_count = 0
        self.frame_width = 640
        self.frame_height = 480
        self.fps = 20
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # Inisialisasi video writer
        self.video_writer_raw = None
        self.video_writer_bbox = None
        self.is_recording = False  # Status perekaman

    def start_recording(self):
        """Mulai perekaman video"""
        if not self.is_recording:
            self.is_recording = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_filename = os.path.join(output_dir, f"raw_{timestamp}.mp4")
            bbox_filename = os.path.join(output_dir, f"bbox_{timestamp}.mp4")
            self.video_writer_raw = cv2.VideoWriter(raw_filename, self.fourcc, self.fps, (self.frame_width, self.frame_height))
            self.video_writer_bbox = cv2.VideoWriter(bbox_filename, self.fourcc, self.fps, (self.frame_width, self.frame_height))
            print(f"Perekaman dimulai: {raw_filename}, {bbox_filename}")

    def stop_recording(self):
        """Hentikan perekaman video"""
        if self.is_recording:
            self.is_recording = False
            if self.video_writer_raw is not None:
                self.video_writer_raw.release()
            if self.video_writer_bbox is not None:
                self.video_writer_bbox.release()
            self.video_writer_raw = None
            self.video_writer_bbox = None
            print("Perekaman dihentikan.")

    def process_image(self, img):
        """Proses deteksi wajah dan simpan frame ke video"""
        try:
            img = cv2.resize(img, (self.frame_width, self.frame_height))
            raw_frame = img.copy()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Simpan ke video saat sedang merekam
            if self.is_recording:
                self.save_video_frames(raw_frame, img)

            return img  # Langsung return frame yang sudah diproses

        except Exception as e:
            print(f"Error processing image: {e}")
            return None


    def save_video_frames(self, raw_frame, bbox_frame):
        """Simpan frame mentah dan frame dengan bounding box ke dalam video"""
        if self.video_writer_raw is not None and self.video_writer_bbox is not None:
            self.video_writer_raw.write(raw_frame)
            self.video_writer_bbox.write(bbox_frame)