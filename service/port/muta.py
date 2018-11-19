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


from eos.db.gamedata.queries import getAttributeInfo
from gui.utils.numberFormatter import roundToPrec


def exportMutant(mutant, firstPrefix='', prefix=''):
    exportLines = []
    mutatedAttrs = {}
    for attrID, mutator in mutant.mutators.items():
        attrName = getAttributeInfo(attrID).name
        mutatedAttrs[attrName] = mutator.value
    exportLines.append('{}{}'.format(firstPrefix, mutant.baseItem.name))
    exportLines.append('{}{}'.format(prefix, mutant.mutaplasmid.item.name))
    # Round to 7th significant number to avoid exporting float errors
    customAttrsLine = ', '.join(
        '{} {}'.format(a, roundToPrec(mutatedAttrs[a], 7))
        for a in sorted(mutatedAttrs))
    exportLines.append('{}{}'.format(prefix, customAttrsLine))
    return '\n'.join(exportLines)
