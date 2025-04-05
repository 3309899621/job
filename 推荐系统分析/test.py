import pymysql


def create_database(host, user, password, database_name):
    try:
        # 建立与 MySQL 服务器的连接，不指定数据库名
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # 执行创建数据库的 SQL 语句
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {database_name}"
            cursor.execute(create_db_query)
        # 提交事务
        connection.commit()
        print(f"数据库 {database_name} 创建成功")
    except pymysql.Error as e:
        print(f"创建数据库时出错: {e}")
    finally:
        if connection:
            # 关闭数据库连接
            connection.close()


def execute_sql_file(file_path, host, user, password, database):
    try:
        # 建立数据库连接
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            # 读取 SQL 文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                sql = file.read()
                # 将 SQL 语句按分号分割成多个语句
                statements = sql.split(';')
                for statement in statements:
                    # 去除前后空格
                    statement = statement.strip()
                    if statement:
                        try:
                            # 执行 SQL 语句
                            cursor.execute(statement)
                        except pymysql.Error as e:
                            print(f"执行 SQL 语句时出错: {e}")
        # 提交事务
        connection.commit()
        print(f"SQL 文件 {file_path} 执行成功")
    except pymysql.Error as e:
        print(f"数据库连接出错: {e}")
    finally:
        if connection:
            # 关闭数据库连接
            connection.close()


# 配置信息
host = 'localhost'
user = 'root'
password = 'password'
database_name = 'lagou_db'
sql_file_path = 'lagou_db_jobs.sql'

# 创建数据库
create_database(host, user, password, database_name)

# 执行 SQL 文件到新创建的数据库
execute_sql_file(sql_file_path, host, user, password, database_name)