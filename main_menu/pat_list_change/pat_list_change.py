# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from includes.execute import execute
from mysql.connector import Error

from includes.utils import my_clear_session
from includes.utils import ensure_correct_role, ensure_logged_in

pat_list_change_blueprint = Blueprint('pat_list_change', '__name__')

@pat_list_change_blueprint.route('/pat_list_change', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("dezh", "zav")
def do_pat_list_change():
    try:
        pat_list_change_result_back = request.args['pat_list_change_result_back']
    except:
        pat_list_change_result_back = None
    try:
        pat_list_change_out = request.args['out']
    except:
        pat_list_change_out = None
    try:
        pat_list_change_back = request.args['back']
    except:
        pat_list_change_back = None
    try:
        patients_send_delete = request.form['patients_send_delete']
    except:
        patients_send_delete = None
    try:
        patients_send = request.form['patients_send']
    except:
        patients_send = None
    try:
        edit_send = request.form['edit_send']
    except:
        edit_send = None


    if (pat_list_change_result_back != None):
        return redirect('/pat_list_change')
    if (pat_list_change_out != None):
        return render_template('out.html')
    if (pat_list_change_back != None):
        return redirect('/main_menu')

    ###### ---delete patient chosen--- ######
    if (patients_send_delete != None):
        patient = request.form['patients']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status
        cursor = conn.cursor()
        _SQL = """
                delete from patient where P_id = %s;
                """
        result, status = execute(_SQL, cursor, conn, (patient,))
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status

        success_msg = "Пациент успешно удален из базы данных."

        _SQL = """
                select * from patient;
                """
        result, status = select(_SQL, cursor, conn)
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status
           
        if (len(result) < 1):
            result = "Нет доступных пациентов."
            my_clear_session('patient', 'patient_passp')
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        my_clear_session('patient', 'patient_passp')
        return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result, msg=success_msg)      
    ### ---/delete patient chosen--- ###

    ### ---edit patient chosen--- ###
    if (patients_send != None):
        session['patient'] = request.form['patients']

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status
        cursor = conn.cursor()
        _SQL = """
                select * from patient where P_id = %s;
                """
        result, status = select(_SQL, cursor, conn, (session.get('patient'),))
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status

        if (len(result) < 1):
            result = "Неизвестная ошибка. Нет такого пациента."
            my_clear_session('patient', 'patient_passp')
            return render_template('output.html', output=result, nav_buttons=True, back='pat_list_change_result_back')

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in result:
            print(r)
            if (r[1] == 'None'):
                r[1] = 'null'
            res.append(dict(zip(schema, r)))
        result = res



        session['patient_passp'] = result[0]['P_passport']
        return render_template('main_menu/pat_list_change/pat_list_change_edit.html', patient=result)
    ### ---/edit patient chosen--- ###

    ### ---editing--- ###
    if (edit_send != None):
        patient_edit_num = request.form['patient_edit_num']
        patient_edit_passp = request.form['patient_edit_passp']
        patient_edit_addr = request.form['patient_edit_addr']
        patient_edit_birth = request.form['patient_edit_birth']
        patient_edit_income = request.form['patient_edit_income']
        patient_edit_outcom = request.form['patient_edit_outcom']
        patient_edit_diagn = request.form['patient_edit_diagn']
        patient_edit_room = request.form['patient_edit_room']
        patient_edit_doc = request.form['patient_edit_doc']

        if (patient_edit_doc == 'None'):
            patient_edit_doc = 'null'
        if (patient_edit_outcom == ''):
            patient_edit_outcom = 'null'
        

        conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status
        cursor = conn.cursor()

        if (patient_edit_passp != session.get('patient_passp')):
            _SQL = """
                select P_passport from patient where P_passport=%s;
                """
            result, status = select(_SQL, cursor, conn, (patient_edit_passp,))
            if (status):
                my_clear_session('patient', 'patient_passp')
                return status
            if (len(result) > 0):
                my_clear_session('patient', 'patient_passp')
                result = "Пациент уже существует в базе данных."
                return render_template('output.html', output=result, nav_buttons=True, back='pat_list_change_result_back')

        # why?
        if (patient_edit_doc == 'null'):
            _SQL = """
                update patient set P_id = %s, P_passport = %s, P_address = %s,
                P_birth = %s, P_incoming_date = %s, P_outcoming_date = %s, 
                P_diagnosis = %s, PR_id = %s, PDoc_id = null where P_id = %s;
            """
            result, status = execute(_SQL, cursor, conn, (patient_edit_num, patient_edit_passp, patient_edit_addr,
                                    patient_edit_birth, patient_edit_income, patient_edit_outcom,
                                    patient_edit_diagn, patient_edit_room, 
                                    session.get('patient'),))
        else:
            _SQL = """
                    update patient set P_id = %s, P_passport = %s, P_address = %s,
                    P_birth = %s, P_incoming_date = %s, P_outcoming_date = %s, 
                    P_diagnosis = %s, PR_id = %s, PDoc_id = %s where P_id = %s;
                """
            result, status = execute(_SQL, cursor, conn, (patient_edit_num, patient_edit_passp, patient_edit_addr,
                                        patient_edit_birth, patient_edit_income, patient_edit_outcom,
                                        patient_edit_diagn, patient_edit_room, patient_edit_doc, 
                                        session.get('patient'),))

        if (status):
            my_clear_session('patient', 'patient_passp')
            return status

        success_msg = "Новые значения успешно занесены в базу данных."

        _SQL = """
                select * from patient;
                """
        result, status = select(_SQL, cursor, conn)
        if (status):
            my_clear_session('patient', 'patient_passp')
            return status
           
        if (len(result) < 1):
            result = "Нет доступных пациентов."
            my_clear_session('patient', 'patient_passp')
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        my_clear_session('patient', 'patient_passp')
        return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result, msg=success_msg)     
    ### ---/editing--- ###


    ### ---base--- ###
    conn, status = db_connect(session.get('db_user_login'), session.get('db_user_password'), 'localhost', 'hospital')
    if (status):
        my_clear_session('patient', 'patient_passp')
        return status
    cursor = conn.cursor()
    _SQL = """
            select * from patient;
            """
    result, status = select(_SQL, cursor, conn)
    if (status):
        my_clear_session('patient', 'patient_passp')
        return status
        
    if (len(result) < 1):
        result = "Нет доступных пациентов."
        my_clear_session('patient', 'patient_passp')
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    res = []
    schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
    for r in  result:
        res.append(dict(zip(schema, r)))
    result = res
    my_clear_session('patient', 'patient_passp')
    return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result)    
    ### ---/base---###

