import os
import sys

# Turns on debug mode
debug = False

# You can adjust these paths to your needs
# The main pyfa directory which contains run.py 
pyfaPath = os.path.join(os.getcwd(), os.path.dirname(sys.modules['__main__'].__file__))

# Where we store the saved fits etc, default is the current users home directory
savePath = os.path.expanduser(os.path.join("~", ".pyfa"))

# Static EVE Data from the staticdata repository, should be in the staticdata directory in our pyfa directory
staticPath = os.path.join(pyfaPath, "staticdata")

# The database where we store all the fits etc 
saveDB = os.path.join(savePath, "saveddata.db")

# The database where the static EVE data from the datadump is kept.
# WARNING: This is not the standard sqlite datadump but a modified version for EOS
gameDB = os.path.join(staticPath, "eve.db")

## DON'T MODIFY ANYTHING BELOW ##
import eos.config

#Caching modifiers, disable all gamedata caching, its unneeded.
eos.config.gamedataCache = None
# saveddata db location modifier, shouldn't ever need to touch this
eos.config.saveddata_connectionstring = "sqlite:///" + saveDB + "?check_same_thread=False"
eos.config.gamedata_connectionstring = "sqlite:///" + gameDB + "?check_same_thread=False"
