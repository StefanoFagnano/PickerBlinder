import datetime
import json
import sqlite3

from utils.global_const import DB


def query(id):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    query = 'SELECT permission, payload, functions FROM injections WHERE id=?'
    param = [id]
    cur.execute(query, param)
    data = cur.fetchall()
    con.close()
    return data


def operation_query(filename, path, package, type, input):
    now = datetime.now()
    date = now.strftime("%d_%m_%Y_%H_%M_%S")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    query = "INSERT INTO log (apk_name,apk_path,apk_package,operation_type,selected_input) VALUES(?,?,?,?,?)"
    params = [filename, path, package, type, input]
    cur.execute(query, params)
    con.commit()
    con.close()


def get_last_injection():
    query = "SELECT * FROM log WHERE operation_type= 'WRITE' ORDER BY operation_id DESC LIMIT 1;"
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    con.close()
    print(data)
    return data


def get_last_attack_info():
    sql = "SELECT message FROM attack_result ORDER BY id DESC LIMIT 1;"
    con = sqlite3.connect('DB')
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    print(data)
    return data


def attack_log():
    sql = "SELECT date, message FROM attack_result ORDER BY id"
    con = sqlite3.connect('DB')
    cur = con.cursor()
    cur.execute(sql)
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)


def query_second_injection(id):
    con = sqlite3.connect('DB')
    cur = con.cursor()
    query = 'SELECT permission, payload, functions FROM second_injections WHERE id=?'
    param = [id]
    cur.execute(query, param)
    data = cur.fetchall()
    con.close()
    return data