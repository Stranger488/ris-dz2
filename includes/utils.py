# -*- coding: utf-8 -*-

from flask import redirect, session, flash, url_for, request
from functools import wraps

def ensure_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            msg = "Пожалуйста, авторизуйтесь."
            return redirect(url_for('auth.do_auth', is_more=msg))
        return fn(*args, **kwargs)
    return wrapper


def ensure_correct_role(*args1):
    def ensure_correct_user(fn):
        # make sure we preserve the corrent __name__, and __doc__ values for our decorator
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # in the params we have something called id, is it the same as the user logged in?
            is_right = False
            for role in args1:
                if role == session.get('user_role'):
                    is_right = True
            if (is_right == False):
                # if not, redirect them back home
                msg = "Нет прав для этого пункта."
                return redirect(url_for('main_menu.do_main_menu', is_more=msg))

            # otherwise, move on with all the arguments passed in!
            return fn(*args, **kwargs)
        return wrapper
    return ensure_correct_user


