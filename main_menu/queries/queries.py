# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

app = Flask(__name__)

queries_blueprint = Blueprint('queries', '__name__')

@queries_blueprint.route('/queries', methods = ['POST', 'GET'])
def do_queries():
    try:
        queries_out = request.args['out']
    except:
        queries_out = None

    if (queries_out != None):
        return render_template('out.html')



    try:
        queries_back = request.args['back']
    except:
        queries_back = None

    if (queries_back != None):
        return redirect('/main_menu')


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
