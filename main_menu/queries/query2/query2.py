# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query2_blueprint = Blueprint('query2', '__name__')

@query2_blueprint.route('/query2', methods = ['POST', 'GET'])
def do_query2():
    pass