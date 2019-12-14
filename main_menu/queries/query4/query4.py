# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query4_blueprint = Blueprint('query4', '__name__')

@query4_blueprint.route('/query4', methods = ['POST', 'GET'])
def do_query4():
    try:
        query4_result_back = request.args['query4_result_back']
    except:
        query4_result_back = None
    if (query4_result_back != None):
        return redirect('/queries/query4')

    try:
        query4_out = request.args['out']
    except:
        query4_out = None
    if (query4_out != None):
        return render_template('out.html')

    try:
        query4_back = request.args['back']
    except:
        query4_back = None
    if (query4_back != None):
        return redirect('/queries')

    
    try:
        query4_send = request.form['send']
    except:
        query4_send = None
    if (query4_send != None):
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.patient WHERE P_incoming_date=(SELECT MIN(P_incoming_date) FROM hospital.patient);
                """
        try:
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Таких пациентов не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query4_result_back')
        

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query4/query4_result.html', result=result)

    return render_template('main_menu/queries/query4/query4.html')
