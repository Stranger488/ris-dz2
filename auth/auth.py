# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

auth_blueprint = Blueprint('auth', '__name__')

@auth_blueprint.route('/auth', methods = ['POST', 'GET'])
def do_auth():
    pass
