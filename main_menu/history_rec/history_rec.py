# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

history_rec_blueprint = Blueprint('history_rec', '__name__')

@history_rec_blueprint.route('/history_rec', methods = ['POST', 'GET'])
def do_history_rec():
    pass
