# Menggunakan image Python sebagai base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Menyalin file requirements.txt ke dalam container
COPY requirements.txt .

# Menginstall dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh proyek ke dalam container
COPY . .

# Menambahkan PyInstaller ke environment
RUN pip install pyinstaller

# Membuat aplikasi dengan PyInstaller
RUN pyinstaller --onefile --add-data "app/templates:templates" --add-data "app/static:static" --add-data "config.py:." run.py

# Menentukan port yang akan digunakan oleh aplikasi
EXPOSE 5005

# Menjalankan aplikasi Flask
CMD ["./dist/run"]
