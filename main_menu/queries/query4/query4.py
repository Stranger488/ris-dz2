# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query4_blueprint = Blueprint('query4', '__name__')

@query4_blueprint.route('/query4', methods = ['POST', 'GET'])
def do_query4():
    pass