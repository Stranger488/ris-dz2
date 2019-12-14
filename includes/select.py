# -*- coding: utf-8 -*-

import mysql.connector

def select(_SQL, cursor, params=None):
    try:
        cursor.execute(_SQL, params)
        result = cursor.fetchall()
    except mysql.connector.Error as e:
        raise e
    
    return result
