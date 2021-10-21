import pandas
import pymysql
import numpy as np
from app import app
import matplotlib.pyplot as plt
from config import mysql
from flask import jsonify
from flask import flash, request
from flask import Flask, send_file, make_response
from plot import do_plot,do_plot_pie




        
@app.route('/add', methods=['POST'])
def add_emp():
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        _salary = _json['salary']
            
        if _name and _email and _phone and _address and request.method == 'POST':            
            sqlQuery = "INSERT INTO rest_emp(name, email, phone, address,salary) VALUES(%s, %s, %s, %s, %s)"
            bindData = (_name, _email, _phone, _address,_salary)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee added successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address, salary FROM rest_emp")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    
        
"""@app.route('/emp/<int:id>')
def emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM rest_emp WHERE id =%s", id)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route('/show')
def show():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select count(*) from rest_emp")
    for row in cursor:
        totalemps=row[0]
    cursor.execute("select name,salary from rest_emp")
    names=[]
    salaries=[]
    for row in cursor:
        names.append(row[0])
        salaries.append(row[1])
    explode=[0.2 if salaries[x]==max(salaries) else 0 for x in np.arange(0,totalemps)]
    plt.pie(salaries,explode=explode,labels=names,autopct="%1.1f%%",shadow=True)
    plt.show()"""



@app.route('/update', methods=['PUT'])
def update_emp():
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        _salary = _json['salary']          
        # validate the received values
        if _name and _email and _phone and _address and _id and request.method == 'PUT':            
            sqlQuery = "UPDATE rest_emp SET name=%s, email=%s, phone=%s, address=%s, salary=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _id,_salary)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Employee updated successfully!')
            respone.status_code = 200
            return respone
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()
        
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rest_emp WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('Employee deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/plot', methods=['GET'])
def correlation_matrix():
    bytes_obj = do_plot()
    
    return send_file(bytes_obj,
                     attachment_filename='plot.png',
                     mimetype='image/png')


@app.route('/plotp', methods=['GET'])
def correlation_matrix_pie():
    bytes_obj_pie= do_plot_pie()
    
    return send_file(bytes_obj_pie,
                     attachment_filename='plot.png',
                     mimetype='image/png')



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run()
    
