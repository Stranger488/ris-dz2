# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

from includes.utils import ensure_correct_role, ensure_logged_in

app = Flask(__name__)

queries_blueprint = Blueprint('queries', '__name__')

@queries_blueprint.route('/queries', methods = ['POST', 'GET'])
@ensure_logged_in
@ensure_correct_role("zav")
def do_queries():
    try:
        queries_out = request.args['out']
    except:
        queries_out = None
    try:
        queries_back = request.args['back']
    except:
        queries_back = None
    try:
        point = request.args['point']
    except:
        point = None


    if (queries_out != None):
        return render_template('out.html')
    if (queries_back != None):
        return redirect('/main_menu')
    if (point == None):
        return render_template('main_menu/queries/queries.html')
    if (point == '1'):
        return redirect('/queries/query1')
    if (point == '2'):
        return redirect('/queries/query2')
    if (point == '3'):
        return redirect('/queries/query3')
    if (point == '4'):
        return redirect('/queries/query4')
    if (point == '5'):
        return redirect('/queries/query5')
    if (point == '6'):
        return redirect('/queries/query6')
