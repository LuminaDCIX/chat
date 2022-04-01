# coding = utf-8
"""
@author: zhou
@time:2019/6/20 10:33
"""


from flask import render_template, redirect, url_for, request

from app.chain.chain import *
from . import main
import time
import json
from ..socket_conn import socket_send, socket_send_user
import hashlib

class User:
    username = ''

    def is_authenticated(self):
        return self.username != ''

    def gravatar(self, name=None, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        if name is not None:
            email = name + "@hihichat.com"
        else:
            email = self.username + "@hihichat.com"
        myhash = hashlib.md5(email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=myhash, size=size,
                                                                     default=default, rating=rating)


current_user = User()


# ip2user_name = {}

@main.route('/login/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    print(username)
    if username != '' :
        current_user.username = username
        return redirect(url_for('main.index',current_user=current_user))
    return render_template('login.html',current_user=current_user)


@main.route('/logout/')
def logout():
    current_user.username = ''
    return redirect(url_for('main.login'))


@main.route('/')
def home():
    return render_template('index.html',current_user=current_user)


@main.route('/index/')
def index():
    return render_template('index.html', current_user=current_user)


@main.route('/join_private_room/', methods=["GET", 'POST'])
def join_private_room():
    if not current_user.is_authenticated():
        return redirect(url_for('main.login'), current_user=current_user)
    return render_template('join_private_room.html', current_user=current_user)

@main.route('/new_private_room/', methods=["GET", 'POST'])
def new_private_room():
    if not current_user.is_authenticated():
        return redirect(url_for('main.login'), current_user=current_user)
    new_room(current_user.username)
    return redirect(url_for('main.chat', current_user=current_user))

@main.route('/join_private_room_ip/', methods=["GET", 'POST'])
def join_private_room_ip():
    rname = request.form.get('rname', '')
    ip = request.form.get('ipaddr', '')
    register(ip)
    return redirect(url_for('main.chat', rname=rname, current_user=current_user))

@main.route('/chat/', methods=['GET', 'POST'])
def chat():
    rname = request.args.get('rname', "")
    #ulist = r.zrange("chat-" + rname, 0, -1)
    ulist = get_user_list()
    # messages = r.zrange("msg-" + rname, 0, -1, withscores=True)
    messages = get_messages_chain()
    msg_list = []
    print("messages =", messages)
    for i in messages:
        msg_list.append([json.loads(i[0]), i[1]]) #time.strftime("%Y/%m/%d %p%H:%M:%S", time.localtime(i[1]))])
    if current_user.is_authenticated():
        return render_template('chat.html', rname=rname, user_list=ulist, msg_list=msg_list, current_user=current_user)
    else:
        email = "youke" + "@hihichat.com"
        hash = hashlib.md5(email.encode('utf-8')).hexdigest()
        gravatar_url = 'http://www.gravatar.com/avatar/' + hash + '?s=40&d=identicon&r=g'
        return render_template('chat.html', rname=rname, user_list=ulist,
                               msg_list=msg_list, g=gravatar_url)


@main.route('/api/sendchat/<info>', methods=['GET', 'POST'])
def send_chat(info):
    if current_user.is_authenticated():
        #rname = request.form.get("rname", "")
        post(info)
        socket_send(info, current_user.username)
        return info
    else:
        return info

@main.route('/socketrecv', methods=['GET', 'POST'])
def socket_recv():
    username = request.get_json().get('username')
    data = request.get_json().get('data')
    print(data, username)
    socket_send(data, username)
    return "socket recv", 200


@main.route('/socket_recvuser', methods=['GET', 'POST'])
def socket_recv_user():
    username = request.get_json().get('username')
    socket_send_user(username)
    return "socket recvuser", 200
    

def register(ip):
    url = "http://"+my_ip+":5000/client/register"
    data = {'ip': ip, 'username': current_user.username}
    requests.post(url, json=data,timeout=3)

def get_user_list():
    url = "http://"+my_ip+":5000/client/userlist"
    print(url)
    reply = requests.post(url,timeout=3).json()
    print("reply =", reply)
    return reply['userlist']


def get_messages_chain():
    url = "http://"+my_ip+":5000/client/message"
    reply = requests.post(url,timeout=3).json()
    return reply['message']

def post(message):
    url = "http://"+my_ip+":5000/client/post"
    data = {'msg': message}
    requests.post(url, json=data,timeout=3)

def new_room(username):
    url = "http://"+my_ip+":5000/client/newroom"
    data = {'username': current_user.username}
    requests.post(url,json=data,timeout=3)

