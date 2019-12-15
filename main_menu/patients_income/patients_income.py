# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error
from includes.my_config import DEP_ID

patients_income_blueprint = Blueprint('patients_income', '__name__')

@patients_income_blueprint.route('/patients_income', methods = ['POST', 'GET'])
def do_patients_income():
    try:
        patients_income_result_back = request.args['patients_income_result_back']
    except:
        patients_income_result_back = None
    if (patients_income_result_back != None):
        return redirect('/patients_income')

    try:
        patients_income_out = request.args['out']
    except:
        patients_income_out = None
    if (patients_income_out != None):
        return render_template('out.html')

    try:
        patients_income_back = request.args['back']
    except:
        patients_income_back = None
    if (patients_income_back != None):
        return redirect('/main_menu')

    try:
        patients_income_send = request.form['send']
    except:
        patients_income_send = None
    if (patients_income_send != None):
        session['patient_passp'] = request.form['patient_passp']
        session['patient_addr'] = request.form['patient_addr']
        session['patient_birth'] = request.form['patient_birth']
        session['patient_income'] = request.form['patient_income']
        session['patient_diagn'] = request.form['patient_diagn']


        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                select P_passport, P_outcoming_date from patient where P_passport=%s and P_outcoming_date is null;
                """
            result = select(_SQL, cursor, (session.get('patient_passp'),))
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)


        if (len(result) > 0):
            session.clear()
            result = "Пациент уже существует в базе данных."
            return render_template('output.html', output=result, nav_buttons=True, back='patients_income_result_back')



        if (session.get('available_rooms')):
            return render_template('main_menu/patients_income/patients_income_rooms.html', rooms=session.get('available_rooms'))
        


    try:
        patients_income_rooms_send = request.form['rooms_send']
    except:
        patients_income_rooms_send = None
    if (patients_income_rooms_send != None):
        session['patient_room'] = request.form['patient_room']

        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                insert into patient values (null, %s, %s, %s, %s, null, %s, %s, null);
            """
            cursor.execute(_SQL, (session.get('patient_passp'), session.get('patient_addr'), 
                                    session.get('patient_birth'), session.get('patient_income'),
                                    session.get('patient_diagn'), session.get('patient_room'),))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)

        
        result = "Пациент успешно занесен в базу данных."
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
                select R_id, R_place_count, count(*) as pat_count from room join patient on (room.R_id=patient.PR_id)
                where RDep_id = %s
                group by R_id;
                """
        result = select(_SQL, cursor, (DEP_ID,))
    except Error as e:
        err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True)

    chosen_rooms = []
    for r_id, r_place_count, pat_count in result:
        if (r_place_count > pat_count):
            chosen_rooms.append(r_id)

    if (len(chosen_rooms) < 1):
        result = "Нет свободных палат."
        
        cursor.close()
        conn.close()
        session.clear()
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    session['available_rooms'] = chosen_rooms
    cursor.close()
    conn.close()
    return render_template('main_menu/patients_income/patients_income.html')



    


