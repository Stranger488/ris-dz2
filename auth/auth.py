# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session, g, url_for
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

        conn, status = db_connect(fictive_user_log, fictive_user_passw, 'localhost', 'hospital')
        if (status):
            return status

        cursor = conn.cursor()
        _SQL = """
                select U_id, U_login, U_password, U_user_role from hospital.user where U_login = %s and U_password = %s;  
                """
        result, status = select(_SQL, cursor, conn, (login, scramble,))
        if (status):
            return status

        if (len(result) < 1):
            result = "Неправильный логин или пароль. Попробуйте снова."
            return redirect(url_for('auth.do_auth', is_more=result))

        _SQL = """
                select DB_user_login, DB_user_password, DB_user_role from hospital.db_user where DB_user_id=%s;
                """
        result_db_pas, status = select(_SQL, cursor, conn, (result[0][3],))
        if (status):
            conn.close()
            return status

        if (len(result_db_pas) < 1):
            result = "Неизвестная ошибка. Нет пользователя в базе данных."
            return render_template('auth/auth.html', is_more=result)

        session['user_id'] = result[0][0]
        session['user_log'] = result[0][1]
        session['db_user_login'] = result_db_pas[0][0]
        session['db_user_password'] = result_db_pas[0][1]
        session['user_role'] = result_db_pas[0][2]

        return redirect('/main_menu')

    return render_template('auth/auth.html')


@auth_blueprint.route('/logout')
def do_logout():
    session.pop('user_id', None)
    session.pop('user_log', None)
    session.pop('db_user_login', None)
    session.pop('db_user_password', None)
    session.pop('user_role', None)
    return render_template('out.html')
