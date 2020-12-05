from flask import Flask
from flask import render_template # для рендеринга страницы с ошибкой
import psycopg2

t_host = "127.0.0.1" # либо "localhost", либо доменное имя, либо IP-адрес.
t_port = "5432" # порт postgres по умолчанию
t_dbname = "FedResParsing"
t_user = "postgres"
t_pw = "Vagexyo687"
db_conn = psycopg2.connect( host = t_host , port=t_port , dbname = t_dbname , user = t_user , password = t_pw )
db_cursor = db_conn.cursor( )


def copy_list():
    list_people = ['Frank']
    s = ""
    s += "INSERT INTO tbl_users"
    s += "("
    s += "t_name_user"
    s += ") VALUES ("
    s += "%s"
    s += ")"
    #try:
    db_cursor.execute(s, list_people)
    db_conn.commit()
    #except psycopg2.Error as e:
    #    t_message = "Database error: " + e + "/n SQL: " + s
    #    return render_template("error_page.html", t_message = t_message)
copy_list()
db_cursor.close()
db_conn.close()
