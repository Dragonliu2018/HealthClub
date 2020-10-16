from flask import Flask, request
import config
from exts import db
import json
from flask_msearch import Search

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 载入数据库配置
    db.init_app(app)
    return app

app = create_app()
# 构建数据库
app.app_context().push()
db.create_all(app=create_app())

@app.route('/',methods=['GET','POST'])
def hello_world():
    str = 'Hello world!'
    return str




if __name__ == '__main__':
    app.run()
