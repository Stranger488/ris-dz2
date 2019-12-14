# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query3_blueprint = Blueprint('query3', '__name__')

@query3_blueprint.route('/query3', methods = ['POST', 'GET'])
def do_query3():
    try:
        query3_result_back = request.args['query3_result_back']
    except:
        query3_result_back = None
    if (query3_result_back != None):
        return redirect('/queries/query3')

    try:
        query3_out = request.args['out']
    except:
        query3_out = None
    if (query3_out != None):
        return render_template('out.html')

    try:
        query3_back = request.args['back']
    except:
        query3_back = None
    if (query3_back != None):
        return redirect('/queries')

    
    try:
        query3_send = request.form['send']
    except:
        query3_send = None
    if (query3_send != None):
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.doctor WHERE Doc_enroll_date=(SELECT MIN(Doc_enroll_date) FROM hospital.doctor) AND Doc_dismiss_date IS NULL;
                """
        try:
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Такого врача не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query3_result_back')
        

        res = []
        schema = ['Doc_id', 'Doc_family', 'Doc_passport', 'Doc_address', 'Doc_birth_year', 'Doc_speciality', 'Doc_enroll_date', 'Doc_dismiss_date', 'DocDep_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query3/query3_result.html', result=result)

    return render_template('main_menu/queries/query3/query3.html')
