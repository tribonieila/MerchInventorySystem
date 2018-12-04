# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------------------------------------------------
#  This is an app-specific example router
#
#  This simple router is used for setting languages from app/languages directory
#  as a part of the application path:  app/<lang>/controller/function
#  Language from default.py or 'en' (if the file is not found) is used as
#  a default_language
#
# See <web2py-root-dir>/examples/routes.parametric.example.py for parameter's detail
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# To enable this route file you must do the steps:
# 1. rename <web2py-root-dir>/examples/routes.parametric.example.py to routes.py
# 2. rename this APP/routes.example.py to APP/routes.py (where APP - is your application directory)
# 3. restart web2py (or reload routes in web2py admin interface)
#
# YOU CAN COPY THIS FILE TO ANY APPLICATION'S ROOT DIRECTORY WITHOUT CHANGES!
# ----------------------------------------------------------------------------------------------------------------------

from gluon.fileutils import abspath
from gluon.languages import read_possible_languages

possible_languages = read_possible_languages(abspath('applications', app))
# ----------------------------------------------------------------------------------------------------------------------
# NOTE! app - is an application based router's parameter with name of an application. E.g.'welcome'
# ----------------------------------------------------------------------------------------------------------------------

routers = {
    app: dict(
        default_language=possible_languages['default'][0],
        languages=[lang for lang in possible_languages if lang != 'default']
    )
}

routers = dict( 
    BASE = dict( 
        default_application='mtc_inv', 
    ) 
) 

# routes_onerror = [
#   ('mtc_inv/400', '/mtc_inv/default/user/login'),
#   ('mtc_inv/*', '/mtc_inv/static/fail.html'),
#   ('*/404', '/mtc_inv/static/cantfind.html'),
#   ('*/*', '/mtc_inv/error/index')
# ]
# error_message = '<html><body><h1>%s</h1></body></html>'
# error_message_ticket = '''<html><body><h1>Internal error</h1>
#      Ticket issued: <a href="/admin/default/ticket/%(ticket)s"
#      target="_blank">%(ticket)s</a></body></html>'''

# ----------------------------------------------------------------------------------------------------------------------
# NOTE! To change language in your application using these rules add this line in one of your models files:
# ----------------------------------------------------------------------------------------------------------------------
#   if request.uri_language: T.force(request.uri_language)
