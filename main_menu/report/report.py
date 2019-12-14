# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

report_blueprint = Blueprint('report', '__name__')

@report_blueprint.route('/report', methods = ['POST', 'GET'])
def do_report():
    try:
        report_result_back = request.args['report_result_back']
    except:
        report_result_back = None
    if (report_result_back != None):
        return redirect('/report')

    try:
        report_out = request.args['out']
    except:
        report_out = None
    if (report_out != None):
        return render_template('out.html')

    try:
        report_back = request.args['back']
    except:
        report_back = None
    if (report_back != None):
        return redirect('/main_menu')

    try:
        report_send = request.form['send']
    except:
        report_send = None
    if (report_send != None):
        report_in_year = request.form['in_year']
        report_in_month = request.form['in_month']
        is_existed = True

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='report_result_back')
    
        cursor = conn.cursor()
        _SQL = """
                SELECT * FROM hospital.otchet WHERE O_year=%s AND O_month=%s;
                """
        try:
            result = select(_SQL, cursor, (report_in_year, report_in_month,))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        
        if (len(result) < 1):
            status = []
            is_existed = False

            cursor.callproc('OTCH', (report_in_year, report_in_month,))
            for r in cursor.stored_results():
                status.append(r.fetchall())
            conn.commit()

            if (status[0][0][0] != 'success'):
                result = ("Неизвестная ошибка %s", status[0][0][0])
                return render_template('output.html', output=result, nav_buttons=True)

            try:
                result = select(_SQL, cursor, (report_in_year, report_in_month,))
            except Error as e:
                err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
                return render_template('err_output.html', err_output=err_output, nav_buttons=True)

            if (len(result) < 1):
                result = "В отчете c текущими параметрами нет строк."
                return render_template('output.html', output=result, nav_buttons=True, back='report_result_back')
        
        res = []
        schema = ['O_id', 'O_dep', 'O_year', 'O_month', 'O_diagn', 'O_count']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        
        return render_template('main_menu/report/report_result.html', result=result, is_existed=is_existed, back='back')

    return render_template('main_menu/report/report.html')
                

