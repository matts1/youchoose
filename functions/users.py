#decorators defined here
import settings
import traceback
import sys
import cgi as html
from models.tables.sessions import get

def require_login(fn):
    return auth_level(fn, True, "/login")

def require_no_login(fn):
    return auth_level(fn, False, "/home")

def require_none(fn):
    return auth_level(fn, None, "")

def get_user(response):
    session_cookie = response.get_secure_cookie("session_id")
    if session_cookie is not None:
        session_cookie = session_cookie.decode('utf-8')
        print "cookie:", session_cookie
        user = get(session_cookie)
        print "user:", user
        if user is not None:
            return user
        else:
            return None
    else:
        return None

def auth_level(fn, req, redirect):
    def wrapper(response, *args):
        user = get_user(response)
        if req == None or (user == None and req == False) or (user != None and req == True):
            try:
                return fn(response, *args, user=user)
            except Exception as err:
                from template_engine.main import render
                exc = traceback.format_exception(*sys.exc_info())
                print("".join(exc))
                exc = "".join([html.escape(line) for line in exc]).split("\n")
                for linenum in range(len(exc)):
                    line = exc[linenum]
                    for index in range(len(line)):
                        if line[index] != " ":
                            break
                    exc[linenum] = "&nbsp" * index * 4 + line[index:]

                render('global/error.html', response, {"error": 500, "debug": settings.DEBUG, "traceback": exc})
        else:
            response.redirect(redirect)
        return None
    return wrapper
