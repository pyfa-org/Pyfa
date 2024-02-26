# =============================================================================
# Copyright (C) 2014 Ryan Holmes
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
# =============================================================================


from logbook import Logger

from service.market import Market


pyfalog = Logger(__name__)


def fetchItem(typeName, eagerCat=False):
    sMkt = Market.getInstance()
    eager = 'group.category' if eagerCat else None
    try:
        item = sMkt.getItem(typeName, eager=eager)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pyfalog.warning('service.port.shared: unable to fetch item "{}"'.format(typeName))
        return None
    if item is None:
        return None
    if sMkt.getPublicityByItem(item):
        return item
    else:
        return None
