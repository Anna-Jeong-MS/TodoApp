import json
import pyodbc

from typing import List
from model.models import Address, InputAddress
from pydantic import parse_obj_as

database = 'basic-workshop'
driver = '{ODBC Driver 17 for SQL Server}'

def get_config():
    filename = './static/db_connection.config'
    
    configJson = {}
    readLines = ''
    
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip()  # 줄 끝의 줄 바꿈 문자를 제거한다.
        readLines = readLines + line
    configJson = json.loads(readLines)
    f.close()

    return configJson

def get_db_connection():
    configJson = get_config()
    
    cnxn_string = 'DRIVER=' + driver + ';SERVER=' + configJson['serverName'] + ';DATABASE=' + database + ';UID=' + configJson['admin'] + ';PWD=' + configJson['password']

    conn = pyodbc.connect(cnxn_string)
    
    return conn

def make_table():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE address
             (id INT IDENTITY(1,1) PRIMARY KEY, first_name TEXT, last_name TEXT, email TEXT, gender TEXT, ip_address TEXT)''')

    init_data_query = '''insert into address (first_name, last_name, email, gender, ip_address) values ('Ramon', 'Veal', 'rveal0@acquirethisname.com', 'Male', '250.222.67.146');
        insert into address (first_name, last_name, email, gender, ip_address) values ('Lorne', 'Blasik', 'lblasik1@tripod.com', 'Female', '81.233.177.225');
        insert into address (first_name, last_name, email, gender, ip_address) values ('Farleigh', 'Forde', 'fforde2@paypal.com', 'Male', '25.178.47.195');
        insert into address (first_name, last_name, email, gender, ip_address) values ('Verna', 'Dudden', 'vdudden3@auda.org.au', 'Female', '173.248.215.245');
        insert into address (first_name, last_name, email, gender, ip_address) values ('Lurline', 'Willavoys', 'lwillavoys4@dot.gov', 'Female', '3.31.161.163');
        '''
    c.execute(init_data_query)
    conn.commit()

    conn.close()


def add_todo(address: InputAddress):
    conn = get_db_connection()

    print(address)

    query = 'INSERT INTO address (first_name, last_name, email, gender, ip_address) VALUES (?, ?, ?, ?, ?)'

    params = (address.first_name, address.last_name, address.email, address.gender, address.ip_address)
    
    cursor = conn.cursor()
    result = cursor.execute(query, params)
    conn.commit()

    cursor.close()
    conn.close()

    return result

def update_todo(address: Address):
    conn = get_db_connection()

    query = "UPDATE address SET first_name = ?, last_name = ? email = ?, gender = ?, ip_address = ? WHERE id = '"+address.id+"'"

    params = (address.first_name, address.last_name, address.email, address.gender, address.ip_address)
    
    cursor = conn.cursor()
    result = cursor.execute(query, params)
    conn.commit()

    cursor.close()
    conn.close()

    return result

def read_todo():
    conn = get_db_connection()

    query = 'SELECT * FROM address'
    
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    todos = []
    for row in results:
        row_dict = dict(zip([column[0] for column in cursor.description], row))
        todos.append(Address.parse_obj(row_dict))

    cursor.close()
    conn.close()
    return todos

