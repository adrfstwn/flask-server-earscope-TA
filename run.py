from app import earscope_app
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

app = earscope_app()

if __name__ == "__main__":
    app.run(debug=True)
