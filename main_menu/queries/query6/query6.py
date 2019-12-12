# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query6_blueprint = Blueprint('query6', '__name__')

@query6_blueprint.route('/query6', methods = ['POST', 'GET'])
def do_query6():
    pass