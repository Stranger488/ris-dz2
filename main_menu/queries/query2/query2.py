# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query2_blueprint = Blueprint('query2', '__name__')

@query2_blueprint.route('/query2', methods = ['POST', 'GET'])
def do_query2():
    try:
        query2_result_back = request.args['query2_result_back']
    except:
        query2_result_back = None
    if (query2_result_back != None):
        return redirect('/queries/query2')

    try:
        query2_out = request.args['out']
    except:
        query2_out = None
    if (query2_out != None):
        return render_template('out.html')

    try:
        query2_back = request.args['back']
    except:
        query2_back = None
    if (query2_back != None):
        return redirect('/queries')

    
    try:
        query2_send = request.form['send']
    except:
        query2_send = None
    if (query2_send != None):
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT Dep_id, Dep_name, Dep_master_family, SUM(R_place_count) as place_count FROM hospital.department JOIN hospital.room ON (department.Dep_id=room.RDep_id) GROUP BY Dep_id;
                """
        try:
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Отделений в госпитале не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query2_result_back')
        

        res = []
        schema = ['Dep_id', 'Dep_name', 'Dep_master_family', 'place_count']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query2/query2_result.html', result=result)

    return render_template('main_menu/queries/query2/query2.html')
