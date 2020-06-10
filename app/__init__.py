from flask import Flask
#导入配置文件
from config import Config
app = Flask(__name__)
#添加配置信息
app.config.from_object(Config)

from app import routes
