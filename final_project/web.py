from flask import Flask, render_template, request, redirect, url_for
from model import cust_input, rf_predict
import mysql.connector

def python_connect_mysql(config, state="", table_name="customer"):
    conn = mysql.connector.connect(**config)
    print("Connection established")

    cursor = conn.cursor()

    if state == 'show_tables':
        cursor.execute("SHOW TABLES;")
        table_names = []
        for i in cursor.fetchall():
            table_names.append(i[0])
        return table_names

    elif state == 'show_col':
        query = "SELECT * FROM " + table_name + ";"
        cursor.execute(query)
        rows = cursor.fetchall()
        col_names = []
        for i in cursor.description:
            col_names.append(i[0])
        return col_names

    else:            
        query = "SELECT * FROM " + table_name + ";"
        cursor.execute(query)
        rows = cursor.fetchall()
        data = []
        index_num = 1    
        for row in rows:
            row_data = []
            row_data.append(index_num)
            index_num += 1
            for i in range(len(row)):
                row_data.append(row[i])
            data.append(row_data)
        return data



config = {
   "host":"dsga2433.mysql.database.azure.com",
   "user":"ruichen",
   "password":"Fred1999.",
   "port": 3306,
   "database":"proj2433",
   "ssl_ca": "/Users/chromium/Documents/School/NYU/22FALL/2433/final_project/DigiCertGlobalRootCA.crt.pem",
   "client_flags": [2048],
   "ssl_disabled": False
}
table_names = python_connect_mysql(config, state='show_tables')

app = Flask(__name__)
@app.route('/')
def home():
   return redirect(url_for('initial_page'))

@app.route('/initial_page')
def initial_page():
   return render_template('home.html')

@app.route('/table', methods=['POST', 'GET'])
def table():
   if request.method == 'POST':
      result = request.form
      table_name = result['table_name']
      col_names = python_connect_mysql(config, state='show_col', table_name=table_name)
      data = python_connect_mysql(config, table_name=table_name)
      return render_template("table.html", table_name=table_name, col_names=col_names, data=data)
   
@app.route('/operation', methods=['POST', 'GET'])
def operation():
   if request.method == 'GET':
      return redirect(url_for('initial_page'))
   else:
      result = request.form
      table_name = result['table_name']
      col_names = python_connect_mysql(config, state='show_col', table_name=table_name)
      data = python_connect_mysql(config, table_name=table_name)
      operation_name = result['operation']

      if operation_name == 'insert':
         return render_template("insert.html", table_name=table_name, col_names=col_names, data=data, operation_name=operation_name)
      elif operation_name == 'delete':
         return render_template("delete.html", table_name=table_name, col_names=col_names, data=data, operation_name=operation_name)
      elif operation_name == 'update':
         return render_template("update.html", table_name=table_name, col_names=col_names, data=data, operation_name=operation_name)



@app.route('/survey', methods=['POST', 'GET'])
def survey():
   if request.method == 'GET':
      return render_template("survey.html")

@app.route('/admin', methods=['POST', 'GET'])
def admin():
   if request.method == 'GET':
      return render_template("admin.html", table_names=table_names)


@app.route('/survey/result', methods=['POST', 'GET'])
def proba():
   if request.method == 'POST':
      result = request.form
      p = rf_predict(cust_input(result))[0]
      return render_template("proba.html", result=result, proba=str(p)+"%")

if __name__ == '__main__':
   app.run(debug = True)