# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
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
    try:
        query2_out = request.args['out']
    except:
        query2_out = None
    try:
        query2_back = request.args['back']
    except:
        query2_back = None
    try:
        query2_send = request.form['send']
    except:
        query2_send = None


    if (query2_result_back != None):
        return redirect('/queries/query2')
    if (query2_out != None):
        return render_template('out.html')
    if (query2_back != None):
        return redirect('/queries')
    if (query2_send != None):
        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT Dep_id, Dep_name, Dep_master_family, SUM(R_place_count) as place_count FROM hospital.department JOIN hospital.room ON (department.Dep_id=room.RDep_id) GROUP BY Dep_id;
                """
        result, status = select(_SQL, cursor, conn)
        if (status): 
            return status
        
        if (len(result) < 1):
            result = "Отделений в госпитале не найдено."
            return render_template('output.html', output=result, nav_buttons=True, back='query2_result_back')
        
        res = []
        schema = ['Dep_id', 'Dep_name', 'Dep_master_family', 'place_count']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/queries/query2/query2_result.html', result=result, back='back')

    return render_template('main_menu/queries/query2/query2.html')
