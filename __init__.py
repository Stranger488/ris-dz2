# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect

from main_menu.main_menu import main_menu_blueprint

app = Flask(__name__)

app.register_blueprint(main_menu_blueprint)

@app.route('/')
@app.route('/main_menu')
def do_init():
    return redirect('/main_menu')

if (__name__ == '__main__'):
    app.run(debug = True)
