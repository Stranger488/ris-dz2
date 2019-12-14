# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query1_blueprint = Blueprint('query1', '__name__')

@query1_blueprint.route('/query1', methods = ['POST', 'GET'])
def do_query1():
    try:
        query1_result_back = request.args['query1_result_back']
    except:
        query1_result_back = None
    if (query1_result_back != None):
        return redirect('/queries/query1')

    try:
        query1_out = request.args['out']
    except:
        query1_out = None
    if (query1_out != None):
        return render_template('out.html')

    try:
        query1_back = request.args['back']
    except:
        query1_back = None
    if (query1_back != None):
        return redirect('/queries')

    
    try:
        query1_send = request.form['send']
    except:
        query1_send = None
    if (query1_send != None):
        query1_dep_num = request.form['dep_num']
        query1_zapros1_year = request.form['zapros1_year']

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT Doc_id, Doc_family, COUNT(*) AS pat_count FROM hospital.doctor JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) JOIN hospital.department ON (doctor.DocDep_id=department.Dep_id) WHERE Dep_name=%s AND year(P_incoming_date)=%s GROUP BY Doc_id;
                """
        try:
            result = select(_SQL, cursor, (query1_dep_num, query1_zapros1_year,))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Пациентов в отделении %s за %s год не найдено." % (query1_dep_num, query1_zapros1_year,)
            return render_template('output.html', output=result, nav_buttons=True, back='query1_result_back')
        

        res = []
        schema = ['Doc_id', 'Doc_family', 'pat_count']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query1/query1_result.html', result=result)

    return render_template('main_menu/queries/query1/query1.html')
