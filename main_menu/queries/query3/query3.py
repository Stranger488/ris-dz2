# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

from includes.utils import ensure_correct_role, ensure_logged_in

query3_blueprint = Blueprint('query3', '__name__')

@query3_blueprint.route('/query3', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("zav")
def do_query3():
    try:
        query3_result_back = request.args['query3_result_back']
    except:
        query3_result_back = None
    try:
        query3_out = request.args['out']
    except:
        query3_out = None
    try:
        query3_back = request.args['back']
    except:
        query3_back = None
    try:
        query3_send = request.form['send']
    except:
        query3_send = None


    if (query3_result_back != None):
        return redirect('/queries/query3')
    if (query3_out != None):
        return render_template('out.html')
    if (query3_back != None):
        return redirect('/queries')
    if (query3_send != None):
        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.doctor WHERE Doc_enroll_date=(SELECT MIN(Doc_enroll_date) FROM hospital.doctor) AND Doc_dismiss_date IS NULL;
                """
        result, status = select(_SQL, cursor, conn)
        if (status): 
            return status

        if (len(result) < 1):
            result = "Такого врача не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query3_result_back')

        res = []
        schema = ['Doc_id', 'Doc_family', 'Doc_passport', 'Doc_address', 'Doc_birth_year', 'Doc_speciality', 'Doc_enroll_date', 'Doc_dismiss_date', 'DocDep_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query3/query3_result.html', result=result, back='back')

    return render_template('main_menu/queries/query3/query3.html')
