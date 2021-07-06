#数据库配置文件
#encoding: utf-8
import os

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT     = '3306'
USERNAME = 'root'
DATABASE = 'sport'
PASSWORD = 'liuzhenlong24'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

MSEARCH_INDEX_NAME = 'whoosh_index'

# simple,whoosh

MSEARCH_BACKEND = 'whoosh'

# 自动生成或更新索引

MSEARCH_ENABLE = True
