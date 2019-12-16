# -*- coding: utf-8 -*-

from flask import render_template
import mysql.connector

def execute(_SQL, cursor, conn, params=None):
    try:
        cursor.execute(_SQL, params)
        conn.commit()
    except mysql.connector.Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        err_output = "Невозможно выполнить запрос к базе данных." +  " " + str(e.errno) + " " + e.msg
        return None, render_template('err_output.html', err_output=err_output, nav_buttons=True, back='back')
    
    return True, None
