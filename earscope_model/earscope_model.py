import cv2
import os
import requests
from datetime import datetime
from flask import Flask
from flask_socketio import SocketIO
from config import Config
import threading

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
        self.fps = 30
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        #self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        
        # Tambahkan atribut untuk menyimpan nama file
        self.raw_filename = None
        self.bbox_filename = None
        
        # Inisialisasi video writer
        self.video_writer_raw = None
        self.video_writer_bbox = None
        self.is_recording = False  # Status perekaman
        
        # Api send
        self.api_url = Config.API_SEND_VIDEO_URL

    def start_recording(self):
        """Mulai perekaman video"""
        if not self.is_recording:
            self.is_recording = True
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            self.raw_filename = os.path.join(output_dir, f"raw_{timestamp}.mp4")
            self.bbox_filename = os.path.join(output_dir, f"bbox_{timestamp}.mp4")

            self.video_writer_raw = cv2.VideoWriter(self.raw_filename, self.fourcc, self.fps, (self.frame_width, self.frame_height))
            self.video_writer_bbox = cv2.VideoWriter(self.bbox_filename, self.fourcc, self.fps, (self.frame_width, self.frame_height))

            print(f"Perekaman dimulai: {self.raw_filename}, {self.bbox_filename}")


    def stop_recording(self):
        """Hentikan perekaman video"""
        if self.is_recording:
            self.is_recording = False

            if self.video_writer_raw is not None:
                self.video_writer_raw.release()
            if self.video_writer_bbox is not None:
                self.video_writer_bbox.release()

            print("Perekaman dihentikan.")
            
            # Kirim ke API setelah perekaman selesai
            self.send_to_api()

            # Reset filename setelah dikirim
            self.video_writer_raw = None
            self.video_writer_bbox = None
            self.raw_filename = None
            self.bbox_filename = None
            
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
            
    def send_to_api(self):
        """Mengirim video yang direkam ke API setelah perekaman selesai"""
        if not self.raw_filename or not self.bbox_filename:
            print("Gagal mengirim video: Nama file tidak ditemukan!")
            return

        if not os.path.exists(self.raw_filename) or not os.path.exists(self.bbox_filename):
            print("Gagal mengirim video: File tidak ditemukan!")
            return

        def upload():
            with open(self.raw_filename, "rb") as raw_video, open(self.bbox_filename, "rb") as processed_video:
                files = {
                    "raw_video": (os.path.basename(self.raw_filename), raw_video, "video/mp4"),
                    "processed_video": (os.path.basename(self.bbox_filename), processed_video, "video/mp4"),
                }

                try:
                    #response = requests.post(self.api_url, headers=self.headers, files=files)
                    response = requests.post(self.api_url, files=files, timeout=30)
                    if response.status_code == 201:
                        print("Video berhasil dikirim ke API!")
                        print(f"API Response: {response.json()}")
                    else:
                        print(f"Gagal mengirim video: {response.status_code}, {response.text}")

                except requests.RequestException as e:
                    print(f"Error mengirim video: {e}")
                    
        threading.Thread(target=upload, daemon=True).start()