import sqlite3, datetime, traceback, os

from utils.loader import ADMIN_TG_ID

path = "data/database.db"

def execute(query: str):
    '''Выполнение SQL-запроса'''
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        cursor.execute(query)
        con.commit()
        data = cursor.fetchall()
        if bool(data): return data
        else: return None
    except Exception as ex:
        print(f"Error!\nException: {ex}\n" + \
        f"Traceback: {traceback.print_exc()}\n" + \
        f"Query : {query}")

def check_db():
    if os.path.exists(path) == False:
        sql_admins = """CREATE TABLE "admins" (
	"id"	INTEGER NOT NULL,
	"tg_id"	INTEGER NOT NULL,
	"nick"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT))"""
        execute(sql_admins)
        sql_users = """CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"tg_id"	INTEGER NOT NULL,
	"ban_state"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT))"""
        execute(sql_users)
        sql_posts = """CREATE TABLE "posts" (
	"id"	INTEGER NOT NULL,
	"user_id"	INTEGER,
	"text"	TEXT,
	FOREIGN KEY("user_id") REFERENCES "users"("id") ON UPDATE SET NULL ON DELETE SET NULL,
	PRIMARY KEY("id" AUTOINCREMENT))"""
        execute(sql_posts)
        sql_files = """CREATE TABLE "files" (
	"id"	INTEGER NOT NULL,
	"post_id"	INTEGER NOT NULL,
	"file_id"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("post_id") REFERENCES "posts"("id") ON UPDATE CASCADE ON DELETE CASCADE)"""
        execute(sql_files)
        sql_post_state = """CREATE TABLE "post_state" (
	"id"	INTEGER NOT NULL,
	"admin_id"	INTEGER NOT NULL,
	"post_id"	INTEGER NOT NULL,
	"msg_id"	INTEGER NOT NULL,
	FOREIGN KEY("admin_id") REFERENCES "admins"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY("post_id") REFERENCES "posts"("id") ON UPDATE CASCADE ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT))"""
        execute(sql_post_state)
        admins.add(ADMIN_TG_ID, "Главный админ")
    if admins.check(ADMIN_TG_ID) == False:
        admins.add(ADMIN_TG_ID, "Главный админ")

#Работа с таблицами в базе данных
class users:
    
    def get_id(telegram_id: int):
        data = execute(f"SELECT id FROM users WHERE tg_id = {telegram_id}")
        if bool(data): return data[0][0]
        else: return None
    
    def get_tg_id(user_id: int):
        data = execute(f"SELECT tg_id FROM users WHERE id = {user_id}")
        if bool(data): return data[0][0]
        else: return None
    
    def find(telegram_id: int):
        data = execute(f"SELECT * FROM users WHERE tg_id = {telegram_id}")
        return bool(data)
    
    def chech_ban(telegram_id: int):
        data = execute(f"SELECT ban_state FROM users WHERE tg_id = {telegram_id}")
        if data[0][0] == 0:
            return True
        else:
            return False
    
    def add(telegram_id: int):
        execute(f"INSERT INTO users (tg_id, ban_state) VALUES ({telegram_id}, 0)")
    
    def ban(telegram_id: int):
        execute(f"UPDATE users SET ban_state = 1 WHERE tg_id = {telegram_id}")
    
    def unban(telegram_id: int):
        execute(f"UPDATE users SET ban_state = 0 WHERE tg_id = {telegram_id}")

class admins:
    
    def add(telegram_id: int, nick: str):
        execute(f"INSERT INTO admins (tg_id, nick) VALUES ({telegram_id}, '{nick}')")
    
    def check(telegram_id: int):
        data = execute(f"SELECT * FROM admins WHERE tg_id = {telegram_id}")
        return bool(data)

    def delete(telegram_id: int):
        execute(f"DELETE FROM admins WHERE tg_id = {telegram_id}")
    
    def get(telegram_id: int):
        data = execute(f"SELECT * FROM admins WHERE tg_id = {telegram_id}")
        if bool(data): return data[0]
        else: return None
    
    def get_all():
        data = execute(f"SELECT * FROM admins")
        return data

class posts:
    
    def add(telegram_id: int, post_text: str or None):
        user_id = users.get_id(telegram_id)
        if post_text != None: execute(f"INSERT INTO posts (user_id, text) VALUES ({user_id}, '{post_text}')")
        else: execute(f"INSERT INTO posts (user_id) VALUES ({user_id})")
        post_id = execute("SELECT MAX(id) FROM posts")
        return int(post_id[0][0])
    
    def get(post_id: int):
        data = execute(f"SELECT * FROM posts WHERE id = {post_id}")
        if bool(data): return data[0]
        else: return None
    
    def delete(post_id: int):
        execute(f"DELETE FROM posts WHERE id = {post_id}")

class files:
    
    def add(post_id: int, file_id: str, file_type: str):
        execute(f"INSERT INTO files (post_id, file_id, type) VALUES ({post_id}, '{file_id}', '{file_type}')")
        row_id = execute("SELECT MAX(id) FROM posts")
        return row_id[0][0]
    
    def get(row_id: int):
        data = execute(f"SELECT * FROM files WHERE id = {row_id}")
        if bool(data): return data[0]
        else: return None
    
    def get_post(post_id: int):
        data = execute(f"SELECT * FROM files WHERE post_id = {post_id}")
        return data
    
    def delete(row_id: int):
        execute(f"DELETE FROM files WHERE id = {row_id}")
    
    def delete_post(post_id: int):
        execute(f"DELETE FROM files WHERE post_id = {post_id}")
    
class post_state:
    
    def add(post_id: int, msg_id: int, admin_id: int):
        execute(f"INSERT INTO post_state (post_id, msg_id, admin_id) VALUES ({post_id}, {msg_id}, {admin_id})")
    
    def delete(post_id: int):
        execute(f"DELETE FROM post_state WHERE post_id = {post_id}")
    
    def get(post_id: int, admin_id: int):
        data = execute(f"SELECT msg_id FROM post_state WHERE post_id = {post_id} AND admin_id = {admin_id}")
        if bool(data): return data[0][0]
        else: return None