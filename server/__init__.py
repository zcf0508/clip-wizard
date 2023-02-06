import os
import sys
from typing import TYPE_CHECKING

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join('./', relative_path)


app = Flask(__name__, static_url_path="", static_folder=resource_path('static'))

# 用户目录下
DATABASE = os.path.join(os.path.expanduser('~'), '.clip-wizard', 'db.sqlite')

init_db = False
# 如果文件不存在，或者文件大小为0
if not os.path.exists(DATABASE) or os.path.getsize(DATABASE) == 0:
    init_db = True
    # 创建数据库文件
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.config["SQLALCHEMY_DATABASE_URI"] = f"{prefix}{DATABASE}"
db = SQLAlchemy(app)

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model

    BaseModel = db.make_declarative_base(Model)
else:
    BaseModel = db.Model

if init_db:
    with app.app_context():
        from server.models.task import Task
        db.create_all()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/hello')
def hello():
    return "Hello, World!"

from server.api_v1 import api_v1

app.register_blueprint(api_v1)
