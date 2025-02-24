# Project Tugas Akhir: Sistem Deteksi Dini Penyakit Telinga Berbasis Deep Learning Terintegrasi Kamera Endoskopi & Website Interaktif

## Setup Project

1. Create Virtual Environment:

    linux
    ```bash
    python3 -m venv venv
    ```
    windows
    ```bash
    python -m venv venv
    ```
1. Use the Virtual Environment:

    linux
    ```bash
    source venv/bin/activate
    ```
    linux
    ```bash
    venv/Scripts/activate
    ```
3. Install Package:
    ```bash
    pip install -r requirements.txt
    ```
2. Run:

    web basedd
    ```bash
    flask run
    ```
    app based
    ```bash
    pyinstaller --onefile --add-data "app/templates:templates" --add-data "app/static:static" --add-data "config.py:." run.py
    ```
    ```bash
    ./dist/run
    ```
