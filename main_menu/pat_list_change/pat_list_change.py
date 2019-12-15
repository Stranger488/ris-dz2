# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error

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
    if (pat_list_change_result_back != None):
        return redirect('/pat_list_change')

    try:
        pat_list_change_out = request.args['out']
    except:
        pat_list_change_out = None
    if (pat_list_change_out != None):
        return render_template('out.html')

    try:
        pat_list_change_back = request.args['back']
    except:
        pat_list_change_back = None
    if (pat_list_change_back != None):
        return redirect('/main_menu')


###### delete patient chosen ######
    try:
        patients_send_delete = request.form['patients_send_delete']
    except:
        patients_send_delete = None
    if (patients_send_delete != None):
        patient = request.form['patients']
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                    delete from patient where P_id = %s;
                    """
            cursor.execute(_SQL, (patient,))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        
        success_msg = "Пациент успешно удален из базы данных."
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                    select * from patient;
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

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        session.clear()
        return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result, msg=success_msg)      
##############

######## edit patient chosen #########
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
                    select * from patient where P_id = %s;
                    """
            result = select(_SQL, cursor, (session.get('patient'),))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        if (len(result) < 1):
            result = "Неизвестная ошибка. Нет такого пациента."
            session.clear()
            return render_template('output.html', output=result, nav_buttons=True, back='pat_list_change_result_back')

        cursor.close()
        conn.close()

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        return render_template('main_menu/pat_list_change/pat_list_change_edit.html', patient=result)
###########

######## editing ########
    try:
        edit_send = request.form['edit_send']
    except:
        edit_send = None
    if (edit_send != None):
        patient_edit_num = request.form['patient_edit_num']
        patient_edit_passp = request.form['patient_edit_passp']
        patient_edit_addr = request.form['patient_edit_addr']
        patient_edit_birth = request.form['patient_edit_birth']
        patient_edit_income = request.form['patient_edit_income']
        patient_edit_outcom = request.form['patient_edit_outcom']
        patient_edit_diagn = request.form['patient_edit_diagn']
        patient_edit_room = request.form['patient_edit_room']


        
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                update patient set P_id = %s, P_passport = %s, P_address = %s,
                P_birth = %s, P_incoming_date = %s, P_outcoming_date = %s, 
                P_diagnosis = %s, PR_id = %s where P_id = %s;
            """
            cursor.execute(_SQL, (patient_edit_num, patient_edit_passp, patient_edit_addr,
                                    patient_edit_birth, patient_edit_income, patient_edit_outcom,
                                    patient_edit_diagn, patient_edit_room,
                                    session.get('patient')))
            conn.commit()
            cursor.close()
            conn.close()
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')

        success_msg = "Новые значения успешно занесены в базу данных."
        try:
            conn = db_connect('root', '', 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                    select * from patient;
                    """
            result = select(_SQL, cursor)
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        if (len(result) < 1):
            result = "Нет доступных пациентов."
            session.clear()
            return render_template('output.html', output=result, nav_buttons=True, back='back')

        cursor.close()
        conn.close()

        res = []
        schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
        for r in  result:
            res.append(dict(zip(schema, r)))
        result = res
        session.clear()
        return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result, msg=success_msg)      
################



###### base #####
    try:
        conn = db_connect('root', '', 'localhost', 'hospital')
    except Error as e:
        err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
    try:
        cursor = conn.cursor()
        _SQL = """
                select * from patient;
                """
        result = select(_SQL, cursor)
    except Error as e:
        err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
        session.clear()
        return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
    if (len(result) < 1):
        result = "Нет доступных пациентов."
        session.clear()
        return render_template('output.html', output=result, nav_buttons=True, back='back')

    cursor.close()
    conn.close()

    res = []
    schema = ['P_id', 'P_passport', 'P_address', 'P_birth', 'P_incoming_date', 'P_outcoming_date', 'P_diagnosis', 'PR_id', 'PDoc_id']
    for r in  result:
        res.append(dict(zip(schema, r)))
    result = res

    return render_template('main_menu/pat_list_change/pat_list_change_patients.html', patients=result)

