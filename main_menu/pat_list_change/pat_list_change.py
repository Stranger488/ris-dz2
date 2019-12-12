# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, Blueprint, redirect
from includes.db_connect import db_connect

pat_list_change_blueprint = Blueprint('pat_list_change', '__name__')

@pat_list_change_blueprint.route('/pat_list_change', methods = ['POST', 'GET'])
def do_pat_list_change():
    pass
