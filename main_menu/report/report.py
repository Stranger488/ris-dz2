# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

report_blueprint = Blueprint('report', '__name__')

@report_blueprint.route('/report', methods = ['POST', 'GET'])
def do_report():
    pass
