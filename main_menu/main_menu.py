# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, session, g 
from includes.utils import ensure_logged_in

app = Flask(__name__)

main_menu_blueprint = Blueprint('main_menu', '__name__')

@main_menu_blueprint.route('/main_menu', methods = ['POST', 'GET'])
@ensure_logged_in
def do_main_menu():
    try:
        main_menu_out = request.args['out']
    except:
        main_menu_out = None
    try:
        point = request.args['point']
    except:
        point = None


    if (main_menu_out != None):
        return redirect('/logout')
    if (point == None):
        return render_template('main_menu/main_menu.html')
    if (point == '1'):
        return redirect('/appointment')
    if (point == '2'):
        return redirect('/history_rec')
    if (point == '3'):
        return redirect('/pat_list_change')
    if (point == '4'):
        return redirect('/patients_income')
    if (point == '5'):
        return redirect('/queries')
    if (point == '6'):
        return redirect('/report')

        
@main_menu_blueprint.before_request
def current_user():
    if (session.get('user_log')):
        g.current_user = session.get('user_log')
    else:
        g.current_user = None