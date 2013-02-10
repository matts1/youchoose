#decorators defined here
import settings
import traceback
import sys
import cgi as html

def require_login(fn):
    return auth_level(fn, [1, 4, 5], "/login")

def require_student(fn):
    return auth_level(fn, [4, 5], "/home")

def require_teacher(fn):
    return auth_level(fn, [4, 5], "/home")

def require_admin(fn):
    return auth_level(fn, [5], "/home")

def require_no_login(fn):
    return auth_level(fn, [None], "/home")

def get_level(fn):
    return auth_level(fn, [None, 1, 4, 5], "err")

def get_user(response):
    return None
    session_cookie = response.get_secure_cookie("session_id")
    if session_cookie is not None:
        session_cookie = session_cookie.decode('utf-8')
        user = session.validate(session_cookie)
        if user is not None:
            session.refresh(session_cookie)
            return User(user)
        else:
            return None
    else:
        return None

def auth_level(fn, required_levels, redirect):
    def wrapper(response, *args):
        user = get_user(response)
        if user in required_levels or (user is not None and user.state in required_levels):
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
