from flask import Flask, request
import config
from exts import db
import json
from flask_msearch import Search
from models import StudentInfo, StudentScore, StandardScore, PhysicalTest, RugbyTest, AthleticTest

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

@app.route('/studentinfo',methods=['GET','POST'])
def get_student_info():
    # student_name = str(json.loads(request.values.get("student_name")))
    # grade = int(json.loads(request.values.get("grade")))
    # print(student_name)
    # context = {
    #     'student_name': str(Student.query.all()) # 查询
    # }
    studentinfo_class_list = StudentInfo.query.all()
    studentinfo_dict_list  = []
    studentinfo_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_Tel": "",
        "st_age": ""
    }
    for st in studentinfo_class_list:
        studentinfo_dict["id"] = st.id
        studentinfo_dict["st_name"] = st.st_name
        studentinfo_dict["st_ID"] = st.st_ID
        studentinfo_dict["st_Tel"] = st.st_Tel
        studentinfo_dict["st_age"] = st.st_age

        studentinfo_dict_list.append(studentinfo_dict.copy())#加入列表


    print( studentinfo_dict_list )
    js = json.dumps(studentinfo_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js


if __name__ == '__main__':
    app.run()
