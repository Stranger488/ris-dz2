# -*- coding: utf-8 -*-

from flask import render_template
import mysql.connector

def db_connect(usr: str, passw: str, hst: str, dtbs: str):
    try:
        conn = mysql.connector.connect(
            user = usr,
            password = passw,
            host = hst,
            database = dtbs)
    except mysql.connector.Error as e:
        conn.close()
        err_output = "Невозможно подключиться к базе данных." +  " " + str(e.errno) + " " + e.msg
        return None, render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')

    return conn, None


    