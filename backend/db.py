import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASS = '***REMOVED***'
DB_NAME = 'ecommerce_db'

def connect_db():
    return pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASS, db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
