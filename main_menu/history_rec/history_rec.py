# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

from includes.utils import ensure_correct_role, ensure_logged_in

history_rec_blueprint = Blueprint('history_rec', '__name__')

@history_rec_blueprint.route('/history_rec', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("dezh", "zav", "lech")
def do_history_rec():
    try:
        history_rec_result_back = request.args['history_rec_result_back']
    except:
        history_rec_result_back = None
    if (history_rec_result_back != None):
        return redirect('/history_rec')

    try:
        history_rec_out = request.args['out']
    except:
        history_rec_out = None
    if (history_rec_out != None):
        return render_template('out.html')

    try:
        history_rec_back = request.args['back']
    except:
        history_rec_back = None
    if (history_rec_back != None):
        return redirect('/main_menu')

    try:
        patients_send = request.form['patients_send']
    except:
        patients_send = None
    if (patients_send != None):
        session['patient'] = request.form['patients']

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                    select P_id, PDoc_id from patient where P_id = %s;
                    """
            result = select(_SQL, cursor, (session.get('patient'),))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        if (len(result) < 1):
            result = "Неизвестная ошибка. Нет такого пациента."
            session.clear()
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        cursor.close()
        conn.close()
        return render_template('main_menu/history_rec/history_rec_record.html', patient=result)



    try:
        record_send = request.form['record_send']
    except:
        record_send = None
    if (record_send != None):
        record_date = request.form['record_date']
        record_app = request.form['record_app']

        session['this'] = 1

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                insert into record values (null, %s, %s, %s, %s);
            """
            cursor.execute(_SQL, (record_date, record_app, session.get('this'), session.get('patient'),))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)

        result = "Запись в историю болезни была успешно произведена."
        session.clear()
        return render_template('output.html', output=result, nav_buttons=True, back='back')



    try:
        conn = db_connect('root', '', 'localhost', 'hospital')
    except Error as e:
        err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
    try:
        cursor = conn.cursor()
        _SQL = """
                select P_id, P_passport from patient where P_outcoming_date is null;
                """
        result = select(_SQL, cursor)
    except Error as e:
        err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    if (len(result) < 1):
        result = "Нет доступных пациентов."
        session.clear()
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    cursor.close()
    conn.close()
    return render_template('main_menu/history_rec/history_rec_patients.html', patients=result)
