# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

query6_blueprint = Blueprint('query6', '__name__')

@query6_blueprint.route('/query6', methods = ['POST', 'GET'])
def do_query6():
    try:
        query6_result_back = request.args['query6_result_back']
    except:
        query6_result_back = None
    if (query6_result_back != None):
        return redirect('/queries/query6')

    try:
        query6_out = request.args['out']
    except:
        query6_out = None
    if (query6_out != None):
        return render_template('out.html')

    try:
        query6_back = request.args['back']
    except:
        query6_back = None
    if (query6_back != None):
        return redirect('/queries')

    
    try:
        query6_send = request.form['send']
    except:
        query6_send = None
    if (query6_send != None):
        query6_zapros6_year = request.form['zapros6_year']
        query6_zapros6_month = request.form['zapros6_month']

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    
        cursor = conn.cursor()
        _SQL = """
                SELECT Doc_family FROM hospital.doctor LEFT JOIN (SELECT * FROM hospital.patient WHERE YEAR(P_incoming_date)=%s AND MONTH(P_incoming_date)=%s) p2017_03
	            ON (doctor.Doc_id=p2017_03.PDoc_id) WHERE P_id IS NULL;
                """
        try:
            result = select(_SQL, cursor, (query6_zapros6_year, query6_zapros6_month,))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            result = "Таких врачей не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query6_result_back')
        
        res = []
        schema = ['Doc_family']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query6/query6_result.html', result=result)

    return render_template('main_menu/queries/query6/query6.html')
