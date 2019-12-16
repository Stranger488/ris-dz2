# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from includes.execute import execute
from mysql.connector import Error

from includes.utils import my_clear_session
from includes.utils import ensure_correct_role, ensure_logged_in

appointment_blueprint = Blueprint('appointment', '__name__')

@appointment_blueprint.route('/appointment', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("zav")
def do_appointment():
    try:
        appointment_result_back = request.args['appointment_result_back']
    except:
        appointment_result_back = None
    try:
        appointment_out = request.args['out']
    except:
        appointment_out = None
    try:
        appointment_back = request.args['back']
    except:
        appointment_back = None
    try:
        patients_send = request.form['patients_send']
    except:
        patients_send = None
    try:
        doctors_send = request.form['doctors_send']
    except:
        doctors_send = None

    if (appointment_result_back != None):
        return redirect('/appointment')
    if (appointment_out != None):
        return render_template('out.html')
    if (appointment_back != None):
        return redirect('/main_menu')

    ### ---patient chosen--- ###
    if (patients_send != None):
        session['patient'] = request.form['patients']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient', 'doctor')
            return status
        cursor = conn.cursor()
        _SQL = """
                SELECT Doc_id, Doc_family FROM hospital.doctor LEFT JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) WHERE P_id IS NULL and Doc_dismiss_date IS NULL;
                """
        result, status = select(_SQL, cursor, conn)
        if (status):
            my_clear_session('patient', 'doctor')
            return status

        if (len(result) < 1):
            result = "Нет свободных врачей."
            my_clear_session('patient', 'doctor')
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        return render_template('main_menu/appointment/appointment_doctors.html', doctors=result)
    ### ---/patient chosen--- ###


    ### ---doctor chosen--- ###
    if (doctors_send != None):
        session['doctor'] = request.form['doctors']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient', 'doctor')
            return status
        cursor = conn.cursor()
        _SQL = """
                update patient set PDoc_id=%s where P_id=%s;
            """
        result, status = execute(_SQL, cursor, conn, (session.get('doctor'), session.get('patient'),))
        if (status):
            my_clear_session('patient', 'doctor')
            return status
        result = "Назначение врача прошло успешно."
        my_clear_session('patient', 'doctor')
        return render_template('output.html', output=result, nav_buttons=True, back='back')
    ### ---/doctor chosen--- ###
    

    ### ---base--- ###
    conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
    if (status):
        my_clear_session('patient', 'doctor')
        return status
    cursor = conn.cursor()
    _SQL = """
            select P_id, P_passport from patient where PDoc_id is null;
            """
    result, status = select(_SQL, cursor, conn)
    if (status):
        my_clear_session('patient', 'doctor')
        return status

    if (len(result) < 1):
        result = "Нет пациентов к назначению."
        my_clear_session('patient', 'doctor')
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    return render_template('main_menu/appointment/appointment_patients.html', patients=result)
    ### ---/base--- ###
    

