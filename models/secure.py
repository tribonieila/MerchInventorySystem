############ FORCED SSL #############
# request.requires_https()
# if request.env.http_host.startswith("www."):
#     redirect(URL(host=request.env.http_host[4:]))

############ FORCED SSL #############
# from gluon.settings import global_settings
# if global_settings.cronjob:
#     print 'Running as shell script.'
# elif not request.is_https:
#     redirect(URL(scheme='https', args=request.args, vars=request.vars))
#     session.secure()
#####################################

########## FORCED SSL non-www ##########
# session.secure()
# if not request.is_https:
#     redirect(URL(scheme='https', args=request.args, vars=request.vars))
# request.requires_https()
# if request.env.http_host.startswith("www."):
#     redirect(URL(host=request.env.http_host[4:]))
#####################################