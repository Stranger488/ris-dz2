# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect, url_for, session, flash
import os
import datetime
from includes.my_config import DEP_ID

from includes.utils import ensure_logged_in

from main_menu.main_menu import main_menu_blueprint
from auth.auth import auth_blueprint

from main_menu.appointment.appointment import appointment_blueprint
from main_menu.history_rec.history_rec import history_rec_blueprint
from main_menu.pat_list_change.pat_list_change import pat_list_change_blueprint
from main_menu.patients_income.patients_income import patients_income_blueprint
from main_menu.queries.queries import queries_blueprint
from main_menu.report.report import report_blueprint

from main_menu.queries.query1.query1 import query1_blueprint
from main_menu.queries.query2.query2 import query2_blueprint
from main_menu.queries.query3.query3 import query3_blueprint
from main_menu.queries.query4.query4 import query4_blueprint
from main_menu.queries.query5.query5 import query5_blueprint
from main_menu.queries.query6.query6 import query6_blueprint

app = Flask(__name__)

app.register_blueprint(main_menu_blueprint)
app.register_blueprint(auth_blueprint)

app.register_blueprint(appointment_blueprint)
app.register_blueprint(history_rec_blueprint)
app.register_blueprint(pat_list_change_blueprint)
app.register_blueprint(patients_income_blueprint)
app.register_blueprint(queries_blueprint)
app.register_blueprint(report_blueprint)

app.register_blueprint(query1_blueprint, url_prefix='/queries')
app.register_blueprint(query2_blueprint, url_prefix='/queries')
app.register_blueprint(query3_blueprint, url_prefix='/queries')
app.register_blueprint(query4_blueprint, url_prefix='/queries')
app.register_blueprint(query5_blueprint, url_prefix='/queries')
app.register_blueprint(query6_blueprint, url_prefix='/queries')


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)





app.jinja_env.globals.update(dated_url_for=dated_url_for)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=31)

@app.route('/')
@ensure_logged_in
def do_init():
    return redirect('/main_menu')

if (__name__ == '__main__'):
    app.run(debug = True)
