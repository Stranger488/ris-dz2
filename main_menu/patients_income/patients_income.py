# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from includes.execute import execute
from mysql.connector import Error
from includes.my_config import DEP_ID

from includes.utils import my_clear_session
from includes.utils import ensure_correct_role, ensure_logged_in

patients_income_blueprint = Blueprint('patients_income', '__name__')

@patients_income_blueprint.route('/patients_income', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("dezh")
def do_patients_income():
    try:
        patients_income_result_back = request.args['patients_income_result_back']
    except:
        patients_income_result_back = None
    try:
        patients_income_out = request.args['out']
    except:
        patients_income_out = None
    try:
        patients_income_back = request.args['back']
    except:
        patients_income_back = None
    try:
        patients_income_send = request.form['send']
    except:
        patients_income_send = None
    try:
        patients_income_rooms_send = request.form['rooms_send']
    except:
        patients_income_rooms_send = None


    if (patients_income_result_back != None):
        return redirect('/patients_income')
    if (patients_income_out != None):
        return render_template('out.html')
    if (patients_income_back != None):
        return redirect('/main_menu')
    ### ---patient data gotten--- ###
    if (patients_income_send != None):
        session['patient_passp'] = request.form['patient_passp']
        session['patient_addr'] = request.form['patient_addr']
        session['patient_birth'] = request.form['patient_birth']
        session['patient_income'] = request.form['patient_income']
        session['patient_diagn'] = request.form['patient_diagn']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
            return status
        cursor = conn.cursor()
        _SQL = """
            select P_passport, P_outcoming_date from patient where P_passport=%s and P_outcoming_date is null;
            """
        result, status = select(_SQL, cursor, conn, (session.get('patient_passp'),))
        if (status):
            my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
            return status

        if (len(result) > 0):
            my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
            result = "Пациент уже существует в базе данных."
            return render_template('output.html', output=result, nav_buttons=True, back='patients_income_result_back')

        if (session.get('available_rooms')):
            return render_template('main_menu/patients_income/patients_income_rooms.html', rooms=session.get('available_rooms'))
    ### ---/patient data gotten--- ###

    ### ---room chosen--- ###
    if (patients_income_rooms_send != None):
        session['patient_room'] = request.form['patient_room']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
            return status
        cursor = conn.cursor()
        _SQL = """
                insert into patient values (null, %s, %s, %s, %s, null, %s, %s, null);
                """
        result, status = execute(_SQL, cursor, conn, (session.get('patient_passp'), session.get('patient_addr'), 
                                    session.get('patient_birth'), session.get('patient_income'),
                                    session.get('patient_diagn'), session.get('patient_room'),))
        if (status):
            my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
            return status
 
        result = "Пациент успешно занесен в базу данных."
        my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
        return render_template('output.html', output=result, nav_buttons=True, back='back')
    ### ---/room chosen--- ###

    ### ---available rooms--- ###
    conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
    if (status):
        my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
        return status
    cursor = conn.cursor()
    _SQL = """
            select R_id, R_place_count, count(*) as pat_count from room join patient on (room.R_id=patient.PR_id)
            where RDep_id = %s
            group by R_id;
        """
    result, status = select(_SQL, cursor, conn, (session.get('user_dep'),))
    if (status):
        my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
        return status
    
    chosen_rooms = []
    for r_id, r_place_count, pat_count in result:
        if (r_place_count > pat_count):
            chosen_rooms.append(r_id)

    if (len(chosen_rooms) < 1):
        result = "Нет свободных палат."
        my_clear_session('patient_passp', 'patient_addr', 'patient_birth', 'patient_income', 'patient_diagn', 'patient_room', 'available_rooms')
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    session['available_rooms'] = chosen_rooms
    return render_template('main_menu/patients_income/patients_income.html')
    ### ---/available rooms--- ###


    


