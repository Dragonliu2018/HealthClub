#encoding: utf-8
from exts import db
from datetime import datetime

class StudentInfo(db.Model):
    __tablename__ = 'student_info'
    # __searchable__ = ['student_name'] #指定要索引的字段
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)#主键
    st_name = db.Column(db.String(32),nullable=False, default='no name')#名字
    st_ID = db.Column(db.String(32),nullable=False, default='no ID')#身份证号(唯一)
    st_Tel = db.Column(db.String(32), nullable=False, default='no Tel')#手机号码
    st_age = db.Column(db.Integer, nullable=False, default=0)#年龄

class StudentScore(db.Model):
    __tablename__ = 'student_score'
    # __searchable__ = ['student_name'] #指定要索引的字段
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)#主键
    st_name = db.Column(db.String(32), nullable=False, default='no name')  # 姓名
    st_ID = db.Column(db.String(32), nullable=False, default='no ID')  # 身份证号(唯一)
    test_time = db.Column(db.DateTime, default=datetime.now)#测试时间
    st_age = db.Column(db.Integer, nullable=False, default=0)#年龄
    push_up = db.Column(db.Integer, nullable=False, default=0)#俯卧撑(次)
    plank = db.Column(db.Float, nullable=False, default=0.0)#平板支撑(秒)
    standing_leap = db.Column(db.Float, nullable=False, default=0.0)#立定跳远(米)
    run_20m = db.Column(db.Float, nullable=False, default=0.0)#20米加速跑(秒)
    Pro_Agility = db.Column(db.Float, nullable=False, default=0.0)#Pro Agility(秒)
    T_test = db.Column(db.Float, nullable=False, default=0.0)#T-test(秒)
    Vertical_Jump = db.Column(db.Float, nullable=False, default=0.0)#Vertical Jump(cm)
    suppleness = db.Column(db.Float, nullable=False, default=0.0)#柔韧性(cm)
    age_group = db.Column(db.String(32), nullable=False, default='no age group')#所属年龄组

class StandardScore(db.Model):
    __tablename__ = 'standard_score'
    # __searchable__ = ['student_name'] #指定要索引的字段
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)#主键
    age_group = db.Column(db.String(32), nullable=False, default='no age group')  # 所属年龄组
    push_up = db.Column(db.Integer, nullable=False, default=0)  # 俯卧撑(次)
    plank = db.Column(db.Float, nullable=False, default=0.0)  # 平板支撑(秒)
    standing_leap = db.Column(db.Float, nullable=False, default=0.0)  # 立定跳远(米)
    run_20m = db.Column(db.Float, nullable=False, default=0.0)  # 20米加速跑(秒)
    Pro_Agility = db.Column(db.Float, nullable=False, default=0.0)  # Pro Agility(秒)
    T_test = db.Column(db.Float, nullable=False, default=0.0)  # T-test(秒)
    Vertical_Jump = db.Column(db.Float, nullable=False, default=0.0)  # Vertical Jump(cm)
    suppleness = db.Column(db.Float, nullable=False, default=0.0)  # 柔韧性(cm)
#身体测试表
class PhysicalTest(db.Model):
    __tablename__ = 'physical_test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    st_name = db.Column(db.String(32), nullable=False, default='未知')  # 姓名
    st_ID = db.Column(db.String(32), nullable=False, default='未知')  # 身份证号(唯一)
    st_stature = db.Column(db.Float, nullable=False, default=0.0)  #身高(m)
    st_weight = db.Column(db.Float, nullable=False, default=0.0) # 体重(kg)
    st_grade = db.Column(db.String(32), nullable=False, default='未知')#活动水平(优秀、中等、低下)
    st_age = db.Column(db.Integer, nullable=False, default=0)#年龄
    st_sex = db.Column(db.String(32), nullable=False, default='未知')# 性别
    st_position = db.Column(db.String(32), nullable=False, default='未知')# 运动员专项
#橄榄球测试表
class RugbyTest(db.Model):
    __tablename__ = 'rugby_test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    st_name = db.Column(db.String(32), nullable=False, default='未知')  # 姓名
    st_ID = db.Column(db.String(32), nullable=False, default='未知')  # 身份证号(唯一)
    st_age = db.Column(db.Integer, nullable=False, default=0)  # 年龄+
    st_40yards_dash = db.Column(db.Float, nullable=False, default=0.0)#40码冲刺(秒)
    st_bench_press = db.Column(db.Integer, nullable=False, default=0)# 卧推(个)
    st_vertical_jump = db.Column(db.Float, nullable=False, default=0.0)# 垂直跳（cm）
    st_long_jump = db.Column(db.Float, nullable=False, default=0.0)# 跳远（cm）
    st_20yards_toandfrom = db.Column(db.Float, nullable=False, default=0.0)# 20码往返（s）、
    st_5yards_L = db.Column(db.Float, nullable=False, default=0.0)# L型5码三折跑（s)
    st_60yards_toandfrom = db.Column(db.Float, nullable=False, default=0.0)# 60码往返(S)
#运动能力测试表
class AthleticTest(db.Model):
    __tablename__ = 'athletic_test'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    st_name = db.Column(db.String(32), nullable=False, default='未知')  # 姓名
    st_ID = db.Column(db.String(32), nullable=False, default='未知')  # 身份证号(唯一)
    st_age = db.Column(db.Integer, nullable=False, default=0)  # 年龄+
    st_push_up = db.Column(db.Integer, nullable=False, default=0)  # 俯卧撑(次)标化成绩
    st_plank = db.Column(db.Float, nullable=False, default=0.0)  # 平板支撑(秒)标化成绩
    st_Pro_Agility = db.Column(db.Float, nullable=False, default=0.0)  # Pro Agility(秒)(敏捷性）
    st_suppleness = db.Column(db.Float, nullable=False, default=0.0)  # 柔韧性(cm)（上文的坐位体前屈）
    st_run_20m = db.Column(db.Float, nullable=False, default=0.0)  #20米加速跑(秒)标化成绩
    st_Vertical_Jump = db.Column(db.Float, nullable=False, default=0.0)#Vertical Jump(cm 垂直跳）
    st_T_test = db.Column(db.Float, nullable=False, default=0.0)#T-test（秒）（新加入的值） 一般为0.16s-0.31s