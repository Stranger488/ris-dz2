# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
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
    try:
        query6_out = request.args['out']
    except:
        query6_out = None
    try:
        query6_back = request.args['back']
    except:
        query6_back = None
    try:
        query6_send = request.form['send']
    except:
        query6_send = None


    if (query6_result_back != None):
        return redirect('/queries/query6')
    if (query6_out != None):
        return render_template('out.html')
    if (query6_back != None):
        return redirect('/queries')
    if (query6_send != None):
        query6_zapros6_year = request.form['zapros6_year']
        query6_zapros6_month = request.form['zapros6_month']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT Doc_family FROM hospital.doctor LEFT JOIN (SELECT * FROM hospital.patient WHERE YEAR(P_incoming_date)=%s AND MONTH(P_incoming_date)=%s) p2017_03
	            ON (doctor.Doc_id=p2017_03.PDoc_id) WHERE P_id IS NULL;
                """
        result, status = select(_SQL, cursor, conn, (query6_zapros6_year, query6_zapros6_month,))
        
        if (len(result) < 1):
            result = "Таких врачей не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query6_result_back')
        
        res = []
        schema = ['Doc_family']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query6/query6_result.html', result=result, back='back')

    return render_template('main_menu/queries/query6/query6.html')
