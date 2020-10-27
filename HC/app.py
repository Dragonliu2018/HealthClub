from flask import Flask, request
import config
from exts import db
import json
from flask_msearch import Search
from models import StudentInfo, StudentScore, StandardScore, PhysicalTest, \
    RugbyTest, AthleticTest, FatherTest, ChildTest, ClassInfo
from funcs import get_str_first_aplha
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
    get_str_first_aplha(str)
    return str

#获取大测试
@app.route('/fathertest',methods=['GET','POST'])
def get_father_test():
    fathertest_class_list = FatherTest.query.all()
    fathertest_dict_list  = []
    fathertest_dict = {
        "id": 0,
        "ft_name": "",
    }
    for ft in fathertest_class_list:
        fathertest_dict["id"] = ft.id
        fathertest_dict["ft_name"] = ft.ft_name

        fathertest_dict_list.append(fathertest_dict.copy())#加入列表


    print( fathertest_dict_list )
    js = json.dumps(fathertest_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js

#获取小测试
@app.route('/childtest',methods=['GET','POST'])
def get_child_test():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
    except:
        ft_name = 'null'
    print(ft_name)
    # 查询
    childtest_class_list = ChildTest.query.filter(ChildTest.ft_name == ft_name).all()
    childtest_dict_list  = []
    childtest_dict = {
        "id": 0,
        "ct_name": "",
    }
    for ct in childtest_class_list:
        childtest_dict["id"] = ct.id
        childtest_dict["ct_name"] = ct.ct_name

        childtest_dict_list.append(childtest_dict.copy())#加入列表

    print( childtest_dict_list )
    js = json.dumps(childtest_dict_list)
    return js

#获取班级
@app.route('/classinfo',methods=['GET','POST'])
def get_class_info():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
    except:
        ft_name = 'null'
        ct_name = 'null'
    # 分条件查询
    classinfo_class_list = ClassInfo.query.filter(
        and_(ClassInfo.ft_name == ft_name, ClassInfo.ct_name == ct_name)).all()
    classinfo_dict_list  = []
    classinfo_dict = {
        "id": 0,
        "ft_name": "",
        "ct_name": "",
        "cl_name": "",
    }
    for cl in classinfo_class_list:
        classinfo_dict["id"] = cl.id
        classinfo_dict["ft_name"] = cl.ft_name
        classinfo_dict["ct_name"] = cl.ct_name
        classinfo_dict["cl_name"] = cl.cl_name

        classinfo_dict_list.append(classinfo_dict.copy())#加入列表

    print( classinfo_dict_list )
    js = json.dumps(classinfo_dict_list)
    return js

#获取学生信息
@app.route('/studentinfo',methods=['GET','POST'])
def get_student_info():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        option = int(json.loads(request.values.get("option")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
        st_name = 'null'
        st_age = 0
        option = 0xfff #几乎不可能的值
    # 分条件查询
    if option == 0:#返回所有信息
        studentinfo_class_list = StudentInfo.query.all()
    elif option == 1:#按姓名查找
        studentinfo_class_list = StudentInfo.query.filter(StudentInfo.st_name == st_name).all()
    elif option == 2:#按年龄查找
        if st_age >= 10:
            studentinfo_class_list = StudentInfo.query.filter(StudentInfo.st_age >= st_age).all()
        else:
            studentinfo_class_list = StudentInfo.query.filter(
                and_(StudentInfo.st_age >= st_age, StudentInfo.st_age <= st_age + 2)).all()
    elif option == 3:#大测试+姓名
        studentinfo_class_list = StudentInfo.query.filter(StudentInfo.ft_name == ft_name,
                                                          StudentInfo.st_name == st_name).all()
    elif option == 4:#大测试+年龄段
        if st_age >= 10:
            studentinfo_class_list = db.session.query(StudentInfo).filter(StudentInfo.ft_name == ft_name,
                                                                          StudentInfo.st_age >= st_age).all()
        else:
            studentinfo_class_list = StudentInfo.query.filter(StudentInfo.ft_name == ft_name,
                and_(StudentInfo.st_age >= st_age, StudentInfo.st_age <= st_age + 2)).all()
    elif option == 5:#按照大测试+小测试+班级查找
        studentinfo_class_list = StudentInfo.query.filter(StudentInfo.ft_name == ft_name,
                                                          StudentInfo.ct_name == ct_name,
                                                          StudentInfo.cl_name == cl_name).all()
    elif option == 6:#按照大测试+小测试+班级+姓名查找
        studentinfo_class_list = StudentInfo.query.filter(StudentInfo.ft_name == ft_name,
                                                          StudentInfo.ct_name == ct_name,
                                                          StudentInfo.cl_name == cl_name,
                                                          StudentInfo.st_name == st_name).all()
    elif option == 7:#按照大测试+小测试+班级+年龄段查找
        if st_age >= 10:
            studentinfo_class_list = db.session.query(StudentInfo).filter(StudentInfo.ft_name == ft_name,
                                                                          StudentInfo.ct_name == ct_name,
                                                                          StudentInfo.cl_name == cl_name,
                                                                          StudentInfo.st_age >= st_age).all()
        else:
            studentinfo_class_list = db.session.query(StudentInfo).filter(StudentInfo.ft_name == ft_name,
                                                                          StudentInfo.ct_name == ct_name,
                                                                          StudentInfo.cl_name == cl_name,
                                                                          StudentInfo.st_age >= st_age,
                                                                          StudentInfo.st_age <= st_age + 2).all()
    else:#其他情况
        studentinfo_class_list = []

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
        studentinfo_dict["st_sex"] = st.st_sex

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
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        option = int(json.loads(request.values.get("option")))
        # st_ID = str(json.loads(request.values.get("st_ID")))
        # st_date = str(json.loads(request.values.get("st_date")))
    except:
        ct_name = "null"
        cl_name = "null"
        st_name = "null"
        st_age = 0
        # st_ID = "null"
        # st_date = 'null'
        option = 0xfff  # 几乎不可能的值
    # 分条件查询
    if option == 0:#返回全部
        physicaltest_class_list = PhysicalTest.query.all()
    elif option == 1:#按姓名查找
        physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.st_name==st_name).all()
    elif option == 2:#按年龄段查找
        if st_age >= 10:
            physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.st_age >= st_age).all()
        else:
            physicaltest_class_list = PhysicalTest.query.filter(
                and_(PhysicalTest.st_age >= st_age, PhysicalTest.st_age <= st_age + 2)).all()
    elif option == 3:#按照小测试查找
        physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.ct_name == ct_name).all()
    elif option == 4:#按照按照小测试+班级查找
        physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.ct_name == ct_name,
                                                            PhysicalTest.cl_name == cl_name).all()
    elif option == 5:#按照小测试+班级+姓名查找
        physicaltest_class_list = PhysicalTest.query.filter(PhysicalTest.ct_name == ct_name,
                                                            PhysicalTest.cl_name == cl_name,
                                                            PhysicalTest.st_name == st_name).all()
    elif option == 6:  # 按照小测试+班级+年龄段查找
        if st_age >= 10:
            physicaltest_class_list = db.session.query(PhysicalTest).filter(PhysicalTest.ct_name == ct_name,
                                                  PhysicalTest.cl_name == cl_name,
                                                  PhysicalTest.st_age >= st_age).all()
        else:
            physicaltest_class_list = db.session.query(PhysicalTest).filter(PhysicalTest.ct_name == ct_name,
                                                  PhysicalTest.cl_name == cl_name,
                                                  PhysicalTest.st_age >= st_age,
                                                  PhysicalTest.st_age <= st_age + 2).all()
    else:#其他情况
        physicaltest_class_list = []

    physicaltest_dict_list  = []
    physicaltest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_date": "",
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
        physicaltest_dict["st_date"] = st.st_date
        physicaltest_dict["st_stature"] = st.st_stature
        physicaltest_dict["st_weight"] = st.st_weight
        physicaltest_dict["st_grade"] = st.st_grade
        physicaltest_dict["st_age"] = st.st_age
        physicaltest_dict["st_sex"] = st.st_sex
        physicaltest_dict["st_position"] = st.st_position
        # print(st.st_date.isoformat()[:10])
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
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        option = int(json.loads(request.values.get("option")))
        # st_ID = str(json.loads(request.values.get("st_ID")))
        # st_date = str(json.loads(request.values.get("st_date")))
    except:
        ct_name = "null"
        cl_name = "null"
        st_name = "null"
        st_age = 0
        option = 0xfff  # 几乎不可能的值
    # 分条件查询
    if option == 0:  # 返回全部
        rugbytest_class_list = RugbyTest.query.all()
    elif option == 1:  # 按姓名查找
        rugbytest_class_list = RugbyTest.query.filter(RugbyTest.st_name == st_name).all()
    elif option == 2:  # 按年龄段查找
        if st_age >= 10:
            rugbytest_class_list = RugbyTest.query.filter(RugbyTest.st_age >= st_age).all()
        else:
            rugbytest_class_list = RugbyTest.query.filter(
                and_(RugbyTest.st_age >= st_age, RugbyTest.st_age <= st_age + 2)).all()
    elif option == 3:  # 按照小测试查找
        rugbytest_class_list = RugbyTest.query.filter(RugbyTest.ct_name == ct_name).all()
    elif option == 4:  # 按照按照小测试+班级查找
        rugbytest_class_list = RugbyTest.query.filter(RugbyTest.ct_name == ct_name,
                                                      RugbyTest.cl_name == cl_name).all()
    elif option == 5:  # 按照小测试+班级+姓名查找
        rugbytest_class_list = RugbyTest.query.filter(RugbyTest.ct_name == ct_name,
                                                      RugbyTest.cl_name == cl_name,
                                                      RugbyTest.st_name == st_name).all()
    elif option == 6:  # 按照小测试+班级+年龄段查找
        if st_age >= 10:
            rugbytest_class_list = db.session.query(RugbyTest).filter(RugbyTest.ct_name == ct_name,
                                                                            RugbyTest.cl_name == cl_name,
                                                                            RugbyTest.st_age >= st_age).all()
        else:
            rugbytest_class_list = db.session.query(RugbyTest).filter(RugbyTest.ct_name == ct_name,
                                                                            RugbyTest.cl_name == cl_name,
                                                                            RugbyTest.st_age >= st_age,
                                                                            RugbyTest.st_age <= st_age + 2).all()
    else:  # 其他情况
        rugbytest_class_list = []

    rugbytest_dict_list  = []
    rugbytest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_age": 0,
        "st_date": "",
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
        rugbytest_dict["st_age"] = st.st_age
        rugbytest_dict["st_date"] = st.st_date
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
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_age = int(json.loads(request.values.get("st_age")))
        option = int(json.loads(request.values.get("option")))
    except:
        ct_name = "null"
        cl_name = "null"
        st_name = "null"
        st_age = 0
        option = 0xfff  # 几乎不可能的值
    # 分条件查询
    if option == 0:  # 返回全部
        athletictest_class_list = AthleticTest.query.all()
    elif option == 1:  # 按姓名查找
        athletictest_class_list = AthleticTest.query.filter(AthleticTest.st_name == st_name).all()
    elif option == 2:  # 按年龄段查找
        if st_age >= 10:
            athletictest_class_list = AthleticTest.query.filter(AthleticTest.st_age >= st_age).all()
        else:
            athletictest_class_list = AthleticTest.query.filter(
                and_(AthleticTest.st_age >= st_age, AthleticTest.st_age <= st_age + 2)).all()
    elif option == 3:  # 按照小测试查找
        athletictest_class_list = AthleticTest.query.filter(AthleticTest.ct_name == ct_name).all()
    elif option == 4:  # 按照按照小测试+班级查找
        athletictest_class_list = AthleticTest.query.filter(AthleticTest.ct_name == ct_name,
                                                      AthleticTest.cl_name == cl_name).all()
    elif option == 5:  # 按照小测试+班级+姓名查找
        athletictest_class_list = AthleticTest.query.filter(AthleticTest.ct_name == ct_name,
                                                      AthleticTest.cl_name == cl_name,
                                                      AthleticTest.st_name == st_name).all()
    elif option == 6:  # 按照小测试+班级+年龄段查找
        if st_age >= 10:
            athletictest_class_list = db.session.query(AthleticTest).filter(AthleticTest.ct_name == ct_name,
                                                                      AthleticTest.cl_name == cl_name,
                                                                      AthleticTest.st_age >= st_age).all()
        else:
            athletictest_class_list = db.session.query(AthleticTest).filter(AthleticTest.ct_name == ct_name,
                                                                      AthleticTest.cl_name == cl_name,
                                                                      AthleticTest.st_age >= st_age,
                                                                      AthleticTest.st_age <= st_age + 2).all()
    else:  # 其他情况
        athletictest_class_list = []

    athletictest_dict_list  = []
    athletictest_dict = {
        "id": 0,
        "st_name": "",
        "st_ID": "",
        "st_age": 0,
        "st_date": "",
        "st_push_up": 0,
        "st_plank": 0,
        "st_Pro_Agility": "",
        "st_suppleness": 0,
        "st_run_20m": "",
        "st_Vertical_Jump": "",
        "st_T_test": 0,
        "st_long_jump": 0,
    }
    for st in athletictest_class_list:
        athletictest_dict["id"] = st.id
        athletictest_dict["st_name"] = st.st_name
        athletictest_dict["st_ID"] = st.st_ID
        athletictest_dict["st_age"] = st.st_age
        athletictest_dict["st_date"] = st.st_date
        athletictest_dict["st_push_up"] = st.st_push_up
        athletictest_dict["st_plank"] = st.st_plank
        athletictest_dict["st_Pro_Agility"] = st.st_Pro_Agility
        athletictest_dict["st_suppleness"] = st.st_suppleness
        athletictest_dict["st_run_20m"] = st.st_run_20m
        athletictest_dict["st_Vertical_Jump"] = st.st_Vertical_Jump
        athletictest_dict["st_T_test"] = st.st_T_test
        athletictest_dict["st_long_jump"] = st.st_long_jump

        athletictest_dict_list.append(athletictest_dict.copy())#加入列表


    print( athletictest_dict_list )
    js = json.dumps(athletictest_dict_list)
    # s1 = json.loads(js)
    # print(s1['student_name'][0].grade)
    return js

#添加小测试(安全性！！！)
@app.route('/addchildtest',methods=['GET','POST'])
def add_child_test():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
    except:
        ft_name = 'null'
        ct_name = 'null'
    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试名}不存在！/{小测试名}已存在！"提示语
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if ct:#在大测试下的该小测试已存在
            response['data'] = "false"
            response['message'] =  '<' + ft_name + '-' + ct_name + "> 小测试已存在！"
        else:#满足添加的条件
            childtest = ChildTest(ft_name=ft_name, ct_name=ct_name)
            db.session.add(childtest)
            db.session.commit()
            response['data'] = "true"
            response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

#添加班级(安全性！！！)
@app.route('/addclassinfo',methods=['GET','POST'])
def add_class_info():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试}不存在！/{小测试}不存在！/{班级}已存在！” 提示语
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    cl = ClassInfo.query.filter(ClassInfo.ft_name==ft_name, ClassInfo.ct_name==ct_name,
                                ClassInfo.cl_name==cl_name).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if not ct:#在大测试下的该小测试不存在
            response['data'] = "false"
            response['message'] = '<' + ft_name + '-' + ct_name + "> 小测试不存在！"
        else:
            if cl:#班级已存在
                response['data'] = "false"
                response['message'] =  '<'+ft_name + '-' + ct_name + '-' + cl_name + "> 班级已存在！"
            else:#满足添加的条件
                classinfo = ClassInfo(ft_name=ft_name, ct_name=ct_name, cl_name=cl_name)
                db.session.add(classinfo)
                db.session.commit()
                response['data'] = "true"
                response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

#添加学员(安全性！！！)
@app.route('/addstudentinfo',methods=['GET','POST'])
def add_student_info():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_ID = str(json.loads(request.values.get("st_ID")))
        st_Tel = str(json.loads(request.values.get("st_Tel")))
        st_age = str(json.loads(request.values.get("st_age")))
        st_sex = str(json.loads(request.values.get("st_sex")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
        st_name = 'null'
        st_ID = 'null'
        st_Tel = 'null'
        st_age = 0
        st_sex = 'null'
    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试}不存在！/{小测试}不存在！/{班级}不存在！/{姓名(身份证号)}已存在！”
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    cl = ClassInfo.query.filter(ClassInfo.ft_name==ft_name, ClassInfo.ct_name==ct_name,
                                ClassInfo.cl_name==cl_name).first()
    st = StudentInfo.query.filter(StudentInfo.ft_name == ft_name, StudentInfo.ct_name == ct_name,
                                  StudentInfo.cl_name == cl_name, StudentInfo.st_ID == st_ID).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if not ct:#在大测试下的该小测试不存在
            response['data'] = "false"
            response['message'] = '<' + ft_name + '-' + ct_name + "> 小测试不存在！"
        else:
            if not cl:#班级不存在
                response['data'] = "false"
                response['message'] = '<'+ft_name + '-' + ct_name + '-' + cl_name + "> 班级不存在！"
            else:
                if st:#学员已存在
                    response['data'] = "false"
                    response['message'] = st_name + "(" + st_ID + ") 已存在！"
                else:#满足添加的条件
                    studentinfo = StudentInfo(ft_name=ft_name, ct_name=ct_name, cl_name=cl_name,
                                              st_name=st_name, st_ID=st_ID, st_Tel=st_Tel,
                                              st_age=st_age, st_sex=st_sex)
                    db.session.add(studentinfo)
                    db.session.commit()
                    response['data'] = "true"
                    response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

#添加身体质量测试(安全性！！！)
@app.route('/addphysicaltest',methods=['GET','POST'])
def add_physical_test():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_ID = str(json.loads(request.values.get("st_ID")))
        st_stature = str(json.loads(request.values.get("st_stature")))
        st_weight = str(json.loads(request.values.get("st_weight")))
        st_grade = str(json.loads(request.values.get("st_grade")))
        st_age = str(json.loads(request.values.get("st_age")))
        st_sex = str(json.loads(request.values.get("st_sex")))
        st_position = str(json.loads(request.values.get("st_position")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
        st_name = 'null'
        st_ID = 'null'
        st_stature = 0.0
        st_weight = 0.0
        st_grade = 'null'
        st_age = 0
        st_sex = 'null'
        st_position = 'null'

    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试}不存在！/{小测试}不存在！
                        # /{班级}不存在！/{该同学}不存在！/{该同学(身份证号)}已测试！”
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    cl = ClassInfo.query.filter(ClassInfo.ft_name==ft_name, ClassInfo.ct_name==ct_name,
                                ClassInfo.cl_name==cl_name).first()
    st = StudentInfo.query.filter(StudentInfo.ft_name == ft_name, StudentInfo.ct_name == ct_name,
                                  StudentInfo.cl_name == cl_name, StudentInfo.st_ID == st_ID).first()
    pt = PhysicalTest.query.filter(PhysicalTest.ft_name == ft_name, PhysicalTest.ct_name == ct_name,
                                  PhysicalTest.cl_name == cl_name, PhysicalTest.st_ID == st_ID).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if not ct:#在大测试下的该小测试不存在
            response['data'] = "false"
            response['message'] = '<' + ft_name + '-' + ct_name + "> 小测试不存在！"
        else:
            if not cl:#班级不存在
                response['data'] = "false"
                response['message'] = '<'+ft_name + '-' + ct_name + '-' + cl_name + "> 班级不存在！"
            else:
                if not st:#学员不存在
                    response['data'] = "false"
                    response['message'] = st_name + "(" + st_ID + ") 不存在！"
                else:
                    if pt:
                        response['data'] = "false"
                        response['message'] = st_name + "(" + st_ID + ") 已测试！"
                    else:#满足添加的条件
                        physicaltest = PhysicalTest(ft_name=ft_name, ct_name=ct_name, cl_name=cl_name,
                                                    st_name=st_name, st_ID=st_ID, st_stature=st_stature,
                                                    st_weight=st_weight, st_grade=st_grade, st_age=st_age,
                                                    st_sex=st_sex, st_position=st_position)
                        db.session.add(physicaltest)
                        db.session.commit()
                        response['data'] = "true"
                        response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

#添加橄榄球各项测试(安全性！！！)
@app.route('/addrugbytest',methods=['GET','POST'])
def add_rugby_test():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_ID = str(json.loads(request.values.get("st_ID")))
        st_age = str(json.loads(request.values.get("st_age")))
        st_40yards_dash = str(json.loads(request.values.get("st_40yards_dash")))
        st_bench_press = str(json.loads(request.values.get("st_bench_press")))
        st_vertical_jump = str(json.loads(request.values.get("st_vertical_jump")))
        st_long_jump = str(json.loads(request.values.get("st_long_jump")))
        st_20yards_toandfrom = str(json.loads(request.values.get("st_20yards_toandfrom")))
        st_5yards_L = str(json.loads(request.values.get("st_5yards_L")))
        st_60yards_toandfrom = str(json.loads(request.values.get("st_60yards_toandfrom")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
        st_name = 'null'
        st_ID = 'null'
        st_age = 0
        st_40yards_dash = 0.0
        st_bench_press = 0
        st_vertical_jump = 0.0
        st_long_jump = 0.0
        st_20yards_toandfrom = 0.0
        st_5yards_L = 0.0
        st_60yards_toandfrom = 0.0

    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试}不存在！/{小测试}不存在！
                        # /{班级}不存在！/{该同学}不存在！/{该同学(身份证号)}已测试！”
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    cl = ClassInfo.query.filter(ClassInfo.ft_name==ft_name, ClassInfo.ct_name==ct_name,
                                ClassInfo.cl_name==cl_name).first()
    st = StudentInfo.query.filter(StudentInfo.ft_name == ft_name, StudentInfo.ct_name == ct_name,
                                  StudentInfo.cl_name == cl_name, StudentInfo.st_ID == st_ID).first()
    rt = RugbyTest.query.filter(RugbyTest.ft_name == ft_name, RugbyTest.ct_name == ct_name,
                                  RugbyTest.cl_name == cl_name, RugbyTest.st_ID == st_ID).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if not ct:#在大测试下的该小测试不存在
            response['data'] = "false"
            response['message'] = '<' + ft_name + '-' + ct_name + "> 小测试不存在！"
        else:
            if not cl:#班级不存在
                response['data'] = "false"
                response['message'] = '<'+ft_name + '-' + ct_name + '-' + cl_name + "> 班级不存在！"
            else:
                if not st:#学员不存在
                    response['data'] = "false"
                    response['message'] = st_name + "(" + st_ID + ") 不存在！"
                else:
                    if rt:
                        response['data'] = "false"
                        response['message'] = st_name + "(" + st_ID + ") 已测试！"
                    else:#满足添加的条件
                        rugbytest = RugbyTest(ft_name=ft_name, ct_name=ct_name, cl_name=cl_name,
                                            st_name=st_name, st_ID=st_ID, st_age=st_age,
                                            st_40yards_dash=st_40yards_dash, st_bench_press=st_bench_press,
                                            st_vertical_jump=st_vertical_jump, st_long_jump=st_long_jump,
                                            st_20yards_toandfrom=st_20yards_toandfrom, st_5yards_L=st_5yards_L,
                                            st_60yards_toandfrom=st_60yards_toandfrom)
                        db.session.add(rugbytest)
                        db.session.commit()
                        response['data'] = "true"
                        response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

#添加运动能力测试(安全性！！！)
@app.route('/addathletictest',methods=['GET','POST'])
def add_athletic_test():
    # 小程序端传来数据
    try:
        ft_name = str(json.loads(request.values.get("ft_name")))
        ct_name = str(json.loads(request.values.get("ct_name")))
        cl_name = str(json.loads(request.values.get("cl_name")))
        st_name = str(json.loads(request.values.get("st_name")))
        st_ID = str(json.loads(request.values.get("st_ID")))
        st_age = str(json.loads(request.values.get("st_age")))
        st_push_up = str(json.loads(request.values.get("st_push_up")))
        st_plank = str(json.loads(request.values.get("st_plank")))
        st_Pro_Agility = str(json.loads(request.values.get("st_Pro_Agility")))
        st_suppleness = str(json.loads(request.values.get("st_suppleness")))
        st_run_20m = str(json.loads(request.values.get("st_run_20m")))
        st_Vertical_Jump = str(json.loads(request.values.get("st_Vertical_Jump")))
        st_T_test = str(json.loads(request.values.get("st_T_test")))
        st_long_jump = str(json.loads(request.values.get("st_long_jump")))
    except:
        ft_name = 'null'
        ct_name = 'null'
        cl_name = 'null'
        st_name = 'null'
        st_ID = 'null'
        st_age = 0
        st_push_up = 0
        st_plank = 0.0
        st_Pro_Agility = 0.0
        st_suppleness = 0.0
        st_run_20m = 0.0
        st_Vertical_Jump = 0.0
        st_T_test = 0.0
        st_long_jump = 0.0

    #返回信息
    response = {
        "code": 200,
        "data": "",  # 保存结果：true成功，false失败
        "message": ""  # "添加成功！/{大测试}不存在！/{小测试}不存在！
                        # /{班级}不存在！/{该同学}不存在！/{该同学(身份证号)}已测试！”
    }

    #查询数据库
    ft = FatherTest.query.filter(FatherTest.ft_name == ft_name).first()
    ct = ChildTest.query.filter(ChildTest.ft_name==ft_name, ChildTest.ct_name==ct_name).first()
    cl = ClassInfo.query.filter(ClassInfo.ft_name==ft_name, ClassInfo.ct_name==ct_name,
                                ClassInfo.cl_name==cl_name).first()
    st = StudentInfo.query.filter(StudentInfo.ft_name == ft_name, StudentInfo.ct_name == ct_name,
                                  StudentInfo.cl_name == cl_name, StudentInfo.st_ID == st_ID).first()
    at = AthleticTest.query.filter(AthleticTest.ft_name == ft_name, AthleticTest.ct_name == ct_name,
                                  AthleticTest.cl_name == cl_name, AthleticTest.st_ID == st_ID).first()
    if not ft:#大测试不存在
        response['data'] = "false"
        response['message'] = '<' + ft_name + "> 大测试不存在！"
    else:
        if not ct:#在大测试下的该小测试不存在
            response['data'] = "false"
            response['message'] = '<' + ft_name + '-' + ct_name + "> 小测试不存在！"
        else:
            if not cl:#班级不存在
                response['data'] = "false"
                response['message'] = '<'+ft_name + '-' + ct_name + '-' + cl_name + "> 班级不存在！"
            else:
                if not st:#学员不存在
                    response['data'] = "false"
                    response['message'] = st_name + "(" + st_ID + ") 不存在！"
                else:
                    if at:
                        response['data'] = "false"
                        response['message'] = st_name + "(" + st_ID + ") 已测试！"
                    else:#满足添加的条件
                        athletictest = AthleticTest(ft_name=ft_name, ct_name=ct_name, cl_name=cl_name,
                                            st_name=st_name, st_ID=st_ID, st_age=st_age,
                                            st_push_up=st_push_up, st_plank=st_plank, st_Pro_Agility=st_Pro_Agility,
                                            st_suppleness=st_suppleness, st_run_20m=st_run_20m,
                                            st_Vertical_Jump=st_Vertical_Jump, st_T_test=st_T_test,
                                            st_long_jump=st_long_jump)
                        db.session.add(athletictest)
                        db.session.commit()
                        response['data'] = "true"
                        response['message'] = "添加成功！"

    print( response )
    js = json.dumps(response)
    return js

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)