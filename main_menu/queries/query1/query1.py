# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

query1_blueprint = Blueprint('query1', '__name__')

@query1_blueprint.route('/query1', methods = ['POST', 'GET'])
def do_query1():
    pass