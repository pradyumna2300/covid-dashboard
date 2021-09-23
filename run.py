###############################################################################
#                            RUN MAIN                                         #
###############################################################################
from application.sdp import app
from settings import config



#app.run_server(debug=config.debug, host=config.host, port=config.port)
app.run_server(debug=True)