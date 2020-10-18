from flask import Flask, request
import config
from exts import db
import json
from flask_msearch import Search
from models import StudentInfo, StudentScore, StandardScore, PhysicalTest, RugbyTest, AthleticTest
#部署
from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS
from sqlalchemy import and_

def create_app():
    app = Flask(__name__)
    # 反向代理设置
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app, resources={r"*": {"origins": "*"}})
    CORS(app, supports_credentials=True)

    app.config.from_object(config)  # 载入数据库配置
    db.init_app(app)
    return app

app = create_app()
# 构建数据库
app.app_context().push()
db.create_all(app=create_app())

@app.route('/',methods=['GET','POST'])
def webserver():
    str = 'Dragon Liu!'
    return str

#获取学生信息
@app.route('/studentinfo',methods=['GET','POST'])
def get_student_info():
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

#获取身体质量测试
@app.route('/physicaltest',methods=['GET','POST'])
def get_physical_test():
    # 小程序端传来数据
    try:
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        # print(st_age)
    except:
        st_name = 'null'
        st_age = 0

    # 分条件查询
    if st_name == 'null' and st_age == 0:  # 全部数据
        physicaltest_class_list = PhysicalTest.query.all()
    elif st_name != 'null':
        physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.st_name == st_name).all()
    elif st_age != 0:
        physicaltest_class_list = PhysicalTest.query.filter(
            and_(PhysicalTest.st_age >= st_age, PhysicalTest.st_age <= st_age + 2)).all()
    # physicaltest_class_list = PhysicalTest.query.all()
    physicaltest_dict_list  = []
    physicaltest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_stature": 0.0,
        "st_weight": 0.0,
        "st_grade": "",
        "st_age": 0,
        "st_sex": "",
        "st_position": ""
    }
    for st in physicaltest_class_list:
        physicaltest_dict["id"] = st.id
        physicaltest_dict["st_name"] = st.st_name
        physicaltest_dict["st_ID"] = st.st_ID
        physicaltest_dict["st_stature"] = st.st_stature
        physicaltest_dict["st_weight"] = st.st_weight
        physicaltest_dict["st_grade"] = st.st_grade
        physicaltest_dict["st_age"] = st.st_age
        physicaltest_dict["st_sex"] = st.st_sex
        physicaltest_dict["st_position"] = st.st_position

        physicaltest_dict_list.append(physicaltest_dict.copy())#加入列表


    print( physicaltest_dict_list )
    js = json.dumps(physicaltest_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js

#获取橄榄球各项测试
@app.route('/rugbytest',methods=['GET','POST'])
def get_rugby_test():
    # 小程序端传来数据
    try:
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        # print(st_age)
    except:
        st_name = 'null'
        st_age = 0

    # 分条件查询
    if st_name == 'null' and st_age == 0:  # 全部数据
        rugbytest_class_list = RugbyTest.query.all()
    elif st_name != 'null':
        rugbytest_class_list = RugbyTest.query.filter(RugbyTest.st_name == st_name).all()
    elif st_age != 0:
        rugbytest_class_list = RugbyTest.query.filter(
            and_(RugbyTest.st_age >= st_age, RugbyTest.st_age <= st_age + 2)).all()

    rugbytest_dict_list  = []
    rugbytest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_40yards_dash": 0.0,
        "st_bench_press": 0.0,
        "st_vertical_jump": "",
        "st_long_jump": 0,
        "st_20yards_toandfrom": "",
        "st_5yards_L": "",
        "st_60yards_toandfrom": ""
    }
    for st in rugbytest_class_list:
        rugbytest_dict["id"] = st.id
        rugbytest_dict["st_name"] = st.st_name
        rugbytest_dict["st_ID"] = st.st_ID
        rugbytest_dict["st_40yards_dash"] = st.st_40yards_dash
        rugbytest_dict["st_bench_press"] = st.st_bench_press
        rugbytest_dict["st_vertical_jump"] = st.st_vertical_jump
        rugbytest_dict["st_long_jump"] = st.st_long_jump
        rugbytest_dict["st_20yards_toandfrom"] = st.st_20yards_toandfrom
        rugbytest_dict["st_5yards_L"] = st.st_5yards_L
        rugbytest_dict["st_60yards_toandfrom"] = st.st_60yards_toandfrom

        rugbytest_dict_list.append(rugbytest_dict.copy())#加入列表


    print( rugbytest_dict_list )
    js = json.dumps(rugbytest_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js

#获取运动能力测试
@app.route('/athletictest',methods=['GET','POST'])
def get_athletic_test():
    # 小程序端传来数据
    try:
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        # print(st_age)
    except:
        st_name = 'null'
        st_age = 0

    # 分条件查询
    if st_name == 'null' and st_age == 0:  # 全部数据
        athletictest_class_list = AthleticTest.query.all()
    elif st_name != 'null':
        athletictest_class_list = AthleticTest.query.filter(AthleticTest.st_name == st_name).all()
    elif st_age != 0:
        athletictest_class_list = AthleticTest.query.filter(
            and_(AthleticTest.st_age >= st_age, AthleticTest.st_age <= st_age + 2)).all()

    athletictest_dict_list  = []
    athletictest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_push_up": 0,
        "st_plank": 0,
        "st_Pro_Agility": "",
        "st_suppleness": 0,
        "st_run_20m": "",
        "st_Vertical_Jump": "",
        "st_T_test": 0
    }
    for st in athletictest_class_list:
        athletictest_dict["id"] = st.id
        athletictest_dict["st_name"] = st.st_name
        athletictest_dict["st_ID"] = st.st_ID
        athletictest_dict["st_push_up"] = st.st_push_up
        athletictest_dict["st_plank"] = st.st_plank
        athletictest_dict["st_Pro_Agility"] = st.st_Pro_Agility
        athletictest_dict["st_suppleness"] = st.st_suppleness
        athletictest_dict["st_run_20m"] = st.st_run_20m
        athletictest_dict["st_Vertical_Jump"] = st.st_Vertical_Jump
        athletictest_dict["st_T_test"] = st.st_T_test

        athletictest_dict_list.append(athletictest_dict.copy())#加入列表


    print( athletictest_dict_list )
    js = json.dumps(athletictest_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)