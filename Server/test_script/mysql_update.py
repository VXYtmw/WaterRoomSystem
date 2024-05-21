import pymysql

# 数据库连接配置
DB_HOST = 'localhost'
DB_USER = ''
DB_PASSWORD = ''
DB_NAME = ''
DB_TABLE_NAME = ''

# 连接到 MySQL 数据库
connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             database=DB_NAME,
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # 执行 SQL 查询
        sql = f"UPDATE {DB_TABLE_NAME} SET status = %s, queuing_number = %s WHERE water_room_id = %s"
        status = 1
        queuing_number = 2
        water_room_id = 3
        cursor.execute(sql, (status, queuing_number, water_room_id))
        
    # 提交事务
    connection.commit()

finally:
    # 关闭数据库连接
    connection.close()