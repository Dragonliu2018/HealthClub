from app import app
import json
from models import StudentInfo, StudentScore, StandardScore, PhysicalTest, RugbyTest, AthleticTest
#学生信息接口
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