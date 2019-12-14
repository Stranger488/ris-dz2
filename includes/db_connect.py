# -*- coding: utf-8 -*-

import mysql.connector

def db_connect(usr: str, passw: str, hst: str, dtbs: str):
    try:
        conn = mysql.connector.connect(
            user = usr,
            password = passw,
            host = hst,
            database = dtbs)
    except mysql.connector.Error as e:
        raise e

    return conn
