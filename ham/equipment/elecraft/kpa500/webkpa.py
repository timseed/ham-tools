# Needs moving to Flask
# from ham.kpa500 import Kpa500
# import cherrypy
# import logging
# import os
# from time import sleep
#
#
# class webkpa(object):
#     """
#     This is a Web Interface to the KPA Amplifier
#
#     """
#
#     site_header = """<html>
#                 <head>
#                   <title>Tim's KPA Control for the Web</title>
#                   <link rel="stylesheet" type="text/css" href="/css/rot.css">
#                 </head>
#                 <body>
#                 <h3>V1.0 Read Write</h3>
#                 <hr>
#            """
#     site_end = """  </body>
#            </html>"""
#
#     tab_header = """"<table style="width:100%">
#   <tr>
#     <th>Command</th>
#     <th>Description</th>
#     <th>Value</th>
#     <th>New Value</th>
#   </tr>
#   """
#
#     def __init__(self, config_file):
#         self.l = logging.getLogger(__name__)
#         self.dbg("KPA Web Starting")
#         self.amp = Kpa500(config_file)
#         self.dbg("kpaconfig read and processed")
#         self.cmd = ""
#
#     @cherrypy.expose
#     def index(self):
#         self.dbg("Index being called")
#         rv = webkpa.site_header + webkpa.tab_header
#         rv = rv + """<form action="doit">\n"""
#         cnt = 0
#         for ky in self.amp.cmd.keys():
#             self.dbg("Trying to get value for {}".format(self.amp.cmd[ky]["Msg"]))
#             v = self.amp.get(ky + ";", self.amp.cmd[ky]["Msg"])
#             rv = rv + "<tr><td>{}</td><td>{}</td><td>{}</td>\n".format(
#                 ky, self.amp.cmd[ky]["Msg"], v
#             )
#             if self.amp.cmd[ky]["RW"] == True:
#                 # Add a Text Box to edit values
#                 # Chop the ^ off the Key name
#                 rv = (
#                     rv
#                     + """<td>New Value: <input type="text" name="""
#                     + "{}".format(ky[1:])
#                     + """><br><td></tr>\n"""
#                 )
#                 self.dbg("fld{}".format(cnt))
#                 cnt = cnt + 1
#
#             else:
#                 rv = rv + "<td>Read Only<td></tr>"
#
#         rv = rv + "</table>"
#         rv = rv + """ <input type="submit" value="Submit"></form>"""
#         self.dbg(rv)
#         return rv
#
#     index.exposed = True
#
#     @cherrypy.expose
#     def doit(self, AL, AR, BC, BN, BRP, BRX, DMO, FC, FL, NL, ON, OS, PJ, SP, TR, XI):
#         # Note Only Read/Write fields are passed to this function
#         # The firm did not create a name for the Read Only fields
#         flds = [
#             "AL",
#             "AR",
#             "BC",
#             "BN",
#             "BRP",
#             "BRX",
#             "DMO",
#             "FC",
#             "FL",
#             "NL",
#             "ON",
#             "OS",
#             "PJ",
#             "SP",
#             "TR",
#             "XI",
#         ]
#         vars = [AL, AR, BC, BN, BRP, BRX, DMO, FC, FL, NL, ON, OS, PJ, SP, TR, XI]
#
#         cmd = ""
#         nochange = ""
#         change = ""
#         for v in list(zip(flds, vars)):
#             if len(v[1]) > 0:
#                 change = change + "Field {}:{} <br>".format(v[0], v[1])
#                 # Need to field index as a Param back to the Msg Definition
#                 cmd = cmd + "^{}{};".format(v[0], v[1])
#             else:
#                 nochange = nochange + "Field {}<br>".format(v[0])
#
#         self.cmd = cmd
#
#         return (
#             """ <head>
#                   <title>Update KPA Page</title>
#                   <link rel="stylesheet" type="text/css" href="/css/rot.css">
#                 </head>
#                 <h1>Change</h1>"""
#             + change
#             + """<hl><h2>No Change</h2>"""
#             + nochange
#             + "<h3> Command String is </h3><br>"
#             + cmd
#             + """
#         <form  action="write">\n
#         <h1> PRESS Submit to Write these Changes  (Bottom of page)
#         <br>
#         <h2> Use the Back Button on the Browser to return to the previous page</h2>
#         <br>
#         <input type="submit" value="Submit">
#         </form>
#         """
#         )
#
#     @cherrypy.expose
#     def write(self):
#         self.amp.write(self.cmd)
#         return (
#             """<head>
#                   <title>Update KPA Page</title>
#                   <link rel="stylesheet" type="text/css" href="/css/rot.css">
#                 </head>
#                 <H3>The command has been sent """
#             + self.cmd
#             + """ to KPA500"""
#         )
#
#     def info(self, msg):
#         self.l.info(msg)
#
#     def dbg(self, msg):
#         self.l.debug(msg)
#
#     def err(self, msg):
#         self.l.error(msg)
#
#
# if __name__ == "__main__":
#     import yaml
#     import logging
#     import logging.config
#
#     with open("logging.yaml", "rt") as f:
#         config = yaml.safe_load(f.read())
#         logging.config.dictConfig(config)
#         log = logging.getLogger(__name__)
#         conf = {
#             "/": {
#                 "tools.sessions.on": True,
#                 "tools.staticdir.root": os.path.abspath(os.getcwd()),
#             },
#             "/css": {"tools.staticdir.on": True, "tools.staticdir.dir": "css"},
#             "/static": {"tools.staticdir.on": True, "tools.staticdir.dir": "./public"},
#         }
#
#         cherrypy.config.update({"server.socket_host": "192.168.1.163"})
#         cherrypy.config.update({"server.socket_port": 8000})
#         log.debug("About to start Web Server")
#         cherrypy.quickstart(webkpa("config.yaml"), "/", conf)
