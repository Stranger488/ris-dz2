# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query3_blueprint = Blueprint('query3', '__name__')

@query3_blueprint.route('/query3', methods = ['POST', 'GET'])
def do_query3():
    pass