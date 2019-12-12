# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

appointment_blueprint = Blueprint('appointment', '__name__')

@appointment_blueprint.route('/appointment', methods = ['POST', 'GET'])
def do_appointment():
    pass
