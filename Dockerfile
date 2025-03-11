# Menggunakan image Python sebagai base image
FROM python:3.12-slim

# Install dependencies yang dibutuhkan OpenCV dan PyInstaller
RUN apt-get update && apt-get install -y \
    binutils \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libice6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Membersihkan cache apt

# Set working directory
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstall dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh proyek ke dalam container
COPY . .

# Menambahkan PyInstaller ke environment
# RUN pip install pyinstaller

# Membuat aplikasi dengan PyInstaller
# RUN pyinstaller --onefile --add-data "app/templates:templates" --add-data "app/static:static" --add-data "config.py:." run.py

# Menentukan port yang akan digunakan oleh aplikasi
EXPOSE 5000

# Menjalankan aplikasi dengan Gunicorn
CMD ["gunicorn", "-k", "eventlet", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]
