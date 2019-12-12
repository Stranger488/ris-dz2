# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

patients_income_blueprint = Blueprint('patients_income', '__name__')

@patients_income_blueprint.route('/patients_income', methods = ['POST', 'GET'])
def do_patients_income():
    pass
