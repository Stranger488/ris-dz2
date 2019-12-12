# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect

from main_menu.appointment.appointment import appointment_blueprint
from main_menu.history_rec.history_rec import history_rec_blueprint
from main_menu.pat_list_change.pat_list_change import pat_list_change_blueprint
from main_menu.patients_income.patients_income import patients_income_blueprint
from main_menu.queries.queries import queries_blueprint
from main_menu.report.report import report_blueprint

app = Flask(__name__)

main_menu_blueprint = Blueprint('main_menu', '__name__')

app.register_blueprint(appointment_blueprint)
app.register_blueprint(history_rec_blueprint)
app.register_blueprint(pat_list_change_blueprint)
app.register_blueprint(patients_income_blueprint)
app.register_blueprint(queries_blueprint)
app.register_blueprint(report_blueprint)

@main_menu_blueprint.route('/main_menu', methods = ['POST', 'GET'])
def do_main_menu():
    try:
        out = request.args['out']
    except:
        out = None

    if (out != None):
        return render_template('out.html')

    try:
        point = request.args['point']
    except:
        point = None
    
    if (point == None):
        return render_template('main_menu.html')
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
