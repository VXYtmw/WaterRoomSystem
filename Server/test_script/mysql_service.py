from flask import Flask, request, jsonify
from gevent import pywsgi
import pymysql

app = Flask(__name__)

# 服务器配置
PORT = 443

# 数据库连接配置
DB_HOST = 'localhost'
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_TABLE_NAME = ''

@app.route('/api/get_status', methods=['GET'])
def get_status():
    id = request.args.get('id')  # 获取前端传来的参数 id
    if id is None:
        return jsonify({"error": "Parameter 'id' is required."}), 400
    
    try:
        # 连接MySQL数据库
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        with connection.cursor() as cursor:
            # 执行查询
            sql = f"SELECT status FROM {DB_TABLE_NAME} WHERE water_room_id = %s"
            cursor.execute(sql, (id))
            # 获取查询结果
            result = cursor.fetchone()
            if result:
                status = result[0]
            else:
                status = None
    except Exception as e:
        print("Error:", e)
        status = None
    finally:
        connection.close()
    
    if status is not None:
        # 返回查询结果
        return jsonify({"status": status}), 200
    else:
        return jsonify({"error": "No status found for the given id."}), 404

@app.route('/api/get_number', methods=['GET'])
def get_number():
    id = request.args.get('id')  # 获取前端传来的参数 id
    if id is None:
        return jsonify({"error": "Parameter 'id' is required."}), 400
    
    try:
        # 连接MySQL数据库
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
        with connection.cursor() as cursor:
            # 执行查询
            sql = f"SELECT queuing_number FROM {DB_TABLE_NAME} WHERE water_room_id = %s"
            cursor.execute(sql, (id))
            # 获取查询结果
            result = cursor.fetchone()
            if result:
                number = result[0]
            else:
                number = None
    except Exception as e:
        print("Error:", e)
        number = None
    finally:
        connection.close()
    
    if number is not None:
        # 返回查询结果
        return jsonify({"number": number}), 200
    else:
        return jsonify({"error": "No number found for the given id."}), 404

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', PORT), app)
    server.serve_forever()
