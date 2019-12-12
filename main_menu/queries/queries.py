# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

from main_menu.queries.query1.query1 import query1_blueprint
from main_menu.queries.query2.query2 import query2_blueprint
from main_menu.queries.query3.query3 import query3_blueprint
from main_menu.queries.query4.query4 import query4_blueprint
from main_menu.queries.query5.query5 import query5_blueprint
from main_menu.queries.query6.query6 import query6_blueprint

app = Flask(__name__)

queries_blueprint = Blueprint('queries', '__name__')

app.register_blueprint(query1_blueprint, url_prefix='/queries')
app.register_blueprint(query2_blueprint, url_prefix='/queries')
app.register_blueprint(query3_blueprint, url_prefix='/queries')
app.register_blueprint(query4_blueprint, url_prefix='/queries')
app.register_blueprint(query5_blueprint, url_prefix='/queries')
app.register_blueprint(query6_blueprint, url_prefix='/queries')

@app.route('/queries', methods = ['POST', 'GET'])
def do_queries():
    try:
        back = request.args['back']
    except:
        back = None

    if (back != None):
        return render_template('main_menu.html')


    try:
        point = request.args['point']
    except:
        point = None
    
    if (point == None):
        return render_template('queries.html')
    if (point == '1'):
        return redirect('/query1')
    if (point == '2'):
        return redirect('/query2')
    if (point == '3'):
        return redirect('/query3')
    if (point == '4'):
        return redirect('/query4')
    if (point == '5'):
        return redirect('/query5')
    if (point == '6'):
        return redirect('/query6')
