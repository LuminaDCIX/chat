# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


import os
import sys
from app import create_app, socketio


sys.path.append("./app/chain")


from chain import *

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=8889,)
    # 实例化节点
    t=threading.Thread(target=run)
    t.start()
    q=threading.Thread(target=run_mine)
    q.start()
    event.set()









