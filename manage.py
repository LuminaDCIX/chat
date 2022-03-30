# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


import os
from app import create_app, socketio
from app.chain import *


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=8889,)
    # 实例化节点










