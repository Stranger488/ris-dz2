# -*- coding: utf-8 -*-

import mysql.connector

def db_connect(usr: str, passw: str):
    try:
        conn = mysql.connector.connect(
            user = usr,
            password = passw,
            host = '127.0.0.1',
            database = 'hospital')
    except:
        conn = None

    return conn
