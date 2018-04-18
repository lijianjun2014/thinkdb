from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager #引入登录登入模块
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
#初始化login_manager参数相关
login_manager = LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='login'
login_manager.init_app(app)
