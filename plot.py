import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt
import io

def do_plot():

    conn = pymysql.connect(host="localhost", user="user", passwd="root", db="test")
    cursor = conn.cursor()
    cursor.execute('select * from rest_emp');

    rows = cursor.fetchall()
    """conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM rest_emp")
    rows = cursor.fetchall()"""
    #for x in empRows:
    #df=pd.DataFrame.from_dict(empRows,orient='index')
    str(rows)[0:30]
    df = pd.DataFrame( [[ij for ij in i] for i in rows] )
    df.rename(columns={0: 'id', 1: 'name', 2: 'email', 3: 'phone', 4:'address',5:'salary'}, inplace=True);

    x_pos = np.arange(len(df['name']))
    y=(df['salary'])
    # Create bars
    plt.bar(x_pos, y)
     
    # Create names on the x-axis
    plt.xticks(x_pos,df['name'] )
      
     # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    return bytes_image

def do_plot_pie():

    conn = pymysql.connect(host="localhost", user="user", passwd="root", db="test")
    cursor = conn.cursor()
    cursor.execute('select * from rest_emp');
    rows = cursor.fetchall()
    #conn = mysql.connect()
    #cursor = conn.cursor(pymysql.cursors.DictCursor)
    #cursor.execute("SELECT * FROM rest_emp")
    #rows = cursor.fetchall()
    #for x in empRows:
    #df=pd.DataFrame.from_dict(empRows,orient='index')
    str(rows)[0:30]
    df1 = pd.DataFrame( [[ij for ij in i] for i in rows] )
    df1.rename(columns={0: 'id', 1: 'name', 2: 'email', 3: 'phone', 4:'address',5:'salary'}, inplace=True);
    x_pos1 = np.arange(len(df1['name']))
    
    # Create pie plot
    plt.pie(x_pos1 , labels =df1['name'])
    plt.legend(title = "Names:")
    #plt.show() 
    # here is the trick save your figure into a bytes object and you can afterwards expose it via flas
    bytes_image_pie = io.BytesIO()
    plt.savefig(bytes_image_pie, format='png')
    bytes_image_pie.seek(0)
    return bytes_image_pie
