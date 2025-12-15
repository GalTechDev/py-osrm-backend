import sys
sys.path.insert(0, ".")

#start server
from osrm.server.api import app, init_app
init_app("data/new-caledonia-251208.osm.pbf")
app.run()