# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from includes.execute import execute
from mysql.connector import Error

from includes.utils import my_clear_session
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
    try:
        history_rec_out = request.args['out']
    except:
        history_rec_out = None
    try:
        history_rec_back = request.args['back']
    except:
        history_rec_back = None
    try:
        patients_send = request.form['patients_send']
    except:
        patients_send = None
    try:
        record_send = request.form['record_send']
    except:
        record_send = None


    if (history_rec_result_back != None):
        return redirect('/history_rec')
    if (history_rec_out != None):
        return render_template('out.html')
    if (history_rec_back != None):
        return redirect('/main_menu')

    ### ---patient chosen--- ###
    if (patients_send != None):
        session['patient'] = request.form['patients']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient')
            return status
        cursor = conn.cursor()
        _SQL = """
                select P_id, PDoc_id from patient where P_id = %s;
                """
        result, status = select(_SQL, cursor, conn, (session.get('patient'),))
        if (status):
            my_clear_session('patient')
            return status

        if (len(result) < 1):
            result = "Неизвестная ошибка. Нет такого пациента."
            my_clear_session('patient')
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        return render_template('main_menu/history_rec/history_rec_record.html', patient=result)
    ### ---/patient chosen--- ###

    ### ---record gotten--- ###
    if (record_send != None):
        record_date = request.form['record_date']
        record_app = request.form['record_app']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient')
            return status
        cursor = conn.cursor()
        _SQL = """
                insert into record values (null, %s, %s, %s, %s);
            """
        result, status = execute(_SQL, cursor, conn, (record_date, record_app, session.get('user_id'), session.get('patient'),))
        if (status):
            my_clear_session('patient')
            return status

        result = "Запись в историю болезни была успешно произведена."
        my_clear_session('patient')
        return render_template('output.html', output=result, nav_buttons=True, back='back')
    ### ---/record gotten--- ###

    ### ---base--- ###
    conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
    if (status):
        my_clear_session('patient')
        return status
    cursor = conn.cursor()
    _SQL = """
            select P_id, P_passport from patient where P_outcoming_date is null;
            """
    result, status = select(_SQL, cursor, conn)
    if (status):
        my_clear_session('patient')
        return status

    if (len(result) < 1):
        result = "Нет доступных пациентов."
        my_clear_session('patient')
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    return render_template('main_menu/history_rec/history_rec_patients.html', patients=result)
    ### ---/base--- ###