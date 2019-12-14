# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query5_blueprint = Blueprint('query5', '__name__')

@query5_blueprint.route('/query5', methods = ['POST', 'GET'])
def do_query5():
    try:
        query5_result_back = request.args['query5_result_back']
    except:
        query5_result_back = None
    if (query5_result_back != None):
        return redirect('/queries/query5')

    try:
        query5_out = request.args['out']
    except:
        query5_out = None
    if (query5_out != None):
        return render_template('out.html')

    try:
        query5_back = request.args['back']
    except:
        query5_back = None
    if (query5_back != None):
        return redirect('/queries')

    
    try:
        query5_send = request.form['send']
    except:
        query5_send = None
    if (query5_send != None):
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.doctor LEFT JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) WHERE P_id IS NULL;
                """
        try:
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Таких врачей не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query5_result_back')
        

        res = []
        schema = ['Doc_id', 'Doc_family', 'Doc_passport', 'Doc_address', 'Doc_birth_year', 'Doc_speciality', 'Doc_enroll_date', 'Doc_dismiss_date', 'DocDep_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query5/query5_result.html', result=result, back='back')

    return render_template('main_menu/queries/query5/query5.html')
