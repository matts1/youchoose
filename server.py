from tornado import Server

from os import path
import sys
sys.path.append(path.dirname(path.realpath(__file__)))

from pages import *

server = Server()
server.register('/', index.index)
server.register('/login', login.login)
server.register('/logout', logout.logout)
server.register('/home', home.home)
server.register('/add', add.add)
#server.register(r"/view/(\d+)", )

#this needs to go last, since it's a 404 page
server.register('(.*)', missing.missing)

server.run()

