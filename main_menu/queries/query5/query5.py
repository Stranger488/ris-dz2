# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

from includes.utils import ensure_correct_role, ensure_logged_in

query5_blueprint = Blueprint('query5', '__name__')

@query5_blueprint.route('/query5', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("zav")
def do_query5():
    try:
        query5_result_back = request.args['query5_result_back']
    except:
        query5_result_back = None
    try:
        query5_out = request.args['out']
    except:
        query5_out = None
    try:
        query5_back = request.args['back']
    except:
        query5_back = None
    try:
        query5_send = request.form['send']
    except:
        query5_send = None


    if (query5_result_back != None):
        return redirect('/queries/query5')
    if (query5_out != None):
        return render_template('out.html')
    if (query5_back != None):
        return redirect('/queries')
    if (query5_send != None):
        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.doctor LEFT JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) WHERE P_id IS NULL;
                """
        result, status = select(_SQL, cursor, conn)
        if (status): 
            return status
        
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
