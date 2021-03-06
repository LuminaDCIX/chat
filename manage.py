import os
from app import create_app, socketio
from app.chain import *
import time

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=8889,)
