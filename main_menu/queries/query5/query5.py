# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query5_blueprint = Blueprint('query5', '__name__')

@query5_blueprint.route('/query5', methods = ['POST', 'GET'])
def do_query5():
    pass