from . import render
from functions.users import require_no_login
from models.tables import sessions
from settings import DEVELOPER_KEY
from gdata.youtube.service import *
from gdata.service import BadAuthentication

@require_no_login
def login(response, user):
    email = response.get_field("email")
    password = response.get_field("pwd")
    err = ""
    if email != None and password != None:
        service = YouTubeService()
        service.email = email
        service.password = password
        service.source = 'youtube_interface'
        service.developer_key = DEVELOPER_KEY

        try:
            service.ProgrammaticLogin()
            sessionid = sessions.create(email)
            response.set_secure_cookie("session_id", sessionid)
            response.redirect('/home')
            return

        except BadAuthentication as exception:
            err = str(exception)
    render("users/login.html", response, {"err": err, "email": email})
