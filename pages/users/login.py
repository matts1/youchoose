from . import render
#from functions.users import require_no_login
from settings import DEVELOPER_KEY
from gdata.youtube.service import *
from gdata.service import BadAuthentication

#@require_no_login
def login(response):
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
            response.redirect('/home')
        except BadAuthentication as exception:
            err = str(exception)

#    result = Users().login(email, password)
#    if result == None:
#        err = ""
#    elif result == False:
#        err = "The username or password was incorrect"
#    else:
#        #sessionid = Sessions().register(result.id)
#        #response.set_secure_cookie('session_id', sessionid)
#        return response.redirect("/home")
#    if email == None:
#        email = ""

#    render("users/login.html", response, {"err": err, "email": email})
    render("users/login.html", response, {"err": err, "email": email})
