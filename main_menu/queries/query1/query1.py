# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

from includes.utils import ensure_correct_role, ensure_logged_in

query1_blueprint = Blueprint('query1', '__name__')

@query1_blueprint.route('/query1', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("zav")
def do_query1():
    try:
        query1_result_back = request.args['query1_result_back']
    except:
        query1_result_back = None
    try:
        query1_out = request.args['out']
    except:
        query1_out = None
    try:
        query1_back = request.args['back']
    except:
        query1_back = None
    try:
        query1_send = request.form['send']
    except:
        query1_send = None

    if (query1_result_back != None):
        return redirect('/queries/query1')
    if (query1_out != None):
        return render_template('out.html')
    if (query1_back != None):
        return redirect('/queries')
    if (query1_send != None):
        query1_dep_num = request.form['dep_num']
        query1_zapros1_year = request.form['zapros1_year']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT Doc_id, Doc_family, COUNT(*) AS pat_count FROM hospital.doctor JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) JOIN hospital.department ON (doctor.DocDep_id=department.Dep_id) WHERE Dep_name=%s AND year(P_incoming_date)=%s GROUP BY Doc_id;
                """
        result, status = select(_SQL, cursor, conn, (query1_dep_num, query1_zapros1_year,))
        if (status):
            return status
        if (len(result) < 1):
            result = "Пациентов в отделении %s за %s год не найдено." % (query1_dep_num, query1_zapros1_year,)
            return render_template('output.html', output=result, nav_buttons=True, back='query1_result_back')
        
        res = []
        schema = ['Doc_id', 'Doc_family', 'pat_count']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query1/query1_result.html', result=result, back='back')

    return render_template('main_menu/queries/query1/query1.html')
