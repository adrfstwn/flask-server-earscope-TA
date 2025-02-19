from app import earscope_app  # Import fungsi untuk membuat app

app, socketio = earscope_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)