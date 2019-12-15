# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

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
    if (appointment_result_back != None):
        return redirect('/appointment')

    try:
        appointment_out = request.args['out']
    except:
        appointment_out = None
    if (appointment_out != None):
        return render_template('out.html')

    try:
        appointment_back = request.args['back']
    except:
        appointment_back = None
    if (appointment_back != None):
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
                    SELECT Doc_id, Doc_family FROM hospital.doctor LEFT JOIN hospital.patient ON (doctor.Doc_id=patient.PDoc_id) WHERE P_id IS NULL and Doc_dismiss_date IS NULL;
                    """
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        if (len(result) < 1):
            result = "Нет свободных врачей."
            session.clear()
            return render_template('output.html', output=result, nav_buttons=True, back='back')


        cursor.close()
        conn.close()
        return render_template('main_menu/appointment/appointment_doctors.html', doctors=result)



    try:
        doctors_send = request.form['doctors_send']
    except:
        doctors_send = None
    if (doctors_send != None):
        session['doctor'] = request.form['doctors']

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                update patient set PDoc_id=%s where P_id=%s;
            """
            cursor.execute(_SQL, (session.get('doctor'), session.get('patient'),))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)

        result = "Назначение врача прошло успешно."
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
                select P_id, P_passport from patient where PDoc_id is null;
                """
        result = select(_SQL, cursor)
    except Error as e:
        err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True)
    if (len(result) < 1):
        result = "Нет пациентов к назначению."
        session.clear()
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    cursor.close()
    conn.close()
    return render_template('main_menu/appointment/appointment_patients.html', patients=result)

    

