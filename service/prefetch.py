#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import threading
import config
import os
import eos.types
import eos.db.migration as migration

class PrefetchThread(threading.Thread):
    def run(self):
        # We're a daemon thread, as such, interpreter might get shut down while we do stuff
        # Make sure we don't throw tracebacks to console
        try:
            eos.types.Character.setSkillList(eos.db.getItemsByCategory("Skill", eager=("effects", "attributes", "attributes.info.icon", "attributes.info.unit", "icon")))
        except:
            pass

prefetch = PrefetchThread()
prefetch.daemon = True
prefetch.start()

########
# The following code does not belong here, however until we rebuild skeletons
# to include modified pyfa.py, this is the best place to put it. See GH issue
# #176
# @ todo: move this to pyfa.py
########

#Make sure the saveddata db exists
if not os.path.exists(config.savePath):
    os.mkdir(config.savePath)

if os.path.isfile(config.saveDB):
    # If database exists, run migration after init'd database
    eos.db.saveddata_meta.create_all()
    migration.update(eos.db.saveddata_engine)
else:
    # If database does not exist, do not worry about migration. Simply
    # create and set version
    eos.db.saveddata_meta.create_all()
    eos.db.saveddata_engine.execute('PRAGMA user_version = {}'.format(migration.getAppVersion()))
    #Import default database values
    databaseDefaults.defaultDatabaseValues.importDefaults()
