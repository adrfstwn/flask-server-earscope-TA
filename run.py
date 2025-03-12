# import eventlet
# eventlet.monkey_patch()

from app import create_app, socketio

app = create_app()
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True, port=5000, use_reloader=False)