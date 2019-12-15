# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session, g
from includes.db_connect import db_connect
from includes.select import select
from mysql.connector import Error
import hashlib

auth_blueprint = Blueprint('auth', '__name__')

@auth_blueprint.route('/auth', methods = ['POST', 'GET'])
def do_auth():
    try:
        auth_send = request.form['auth_send']
    except:
        auth_send = None
    if (auth_send != None):
        login = request.form['log']
        password = request.form['passw']
        scramble = hashlib.md5(bytes(password, encoding='utf-8'))
        scramble = scramble.hexdigest()

        fictive_user_log = 'fictive'
        fictive_user_passw = 'qwerty'

        try:
            conn = db_connect(fictive_user_log, fictive_user_passw, 'localhost', 'hospital')
        except Error as e:
            err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
        try:
            cursor = conn.cursor()
            _SQL = """
                    select U_id, U_login, U_password, U_user_role from hospital.user join mysql.user where U_login = %s and U_password = %s;  
                    """
            result = select(_SQL, cursor, (login, scramble,))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        if (len(result) < 1):
            result = "Неправильный логин или пароль. Попробуйте снова."
            return render_template('auth/auth.html', is_more=result)
        
        try:
            cursor = conn.cursor()
            _SQL = """
                    select Password from `mysql`.`user` where User=%s;
                    """
            result_db_pas = select(_SQL, cursor, (result[0][3],))
        except Error as e:
            err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
            session.clear()
            return render_template('err_output.html', err_output=err_output, nav_buttons=True)
        if (len(result) < 1):
            result = "Неизвестная ошибка. Нет пользователя в базе данных."
            return render_template('auth/auth.html', is_more=result)

        session['user_id'] = result[0][0]
        session['user'] = result[0][1]
        session['db_user_login'] = result[0][3]
        session['db_user_password'] = result_db_pas[0][0]
        
        return redirect('/main_menu')

    return render_template('auth/auth.html')


@auth_blueprint.route('/logout')
def do_logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    session.pop('user_password', None)
    session.pop('user', None)
    return render_template('out.html')
