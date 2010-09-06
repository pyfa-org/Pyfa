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

import eos.db
import eos.types

class Character():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Character()

        return cls.instance

    def getCharacterList(self):
        baseChars = [eos.types.Character.getAll0(), eos.types.Character.getAll5()]
        # Flush incase all0 & all5 weren't in the db yet
        eos.db.saveddata_session.flush()
        return map(lambda c: (c.ID, c.name), eos.db.getCharacterList())

    def getSkillGroups(self):
        marketGroup = eos.db.getMarketGroup(150)
        return map(lambda mg: (mg.ID, mg.name), marketGroup.children)

    def getSkills(self, groupID):
        marketGroup = eos.db.getMarketGroup(groupID)
        skills = []
        for skill in marketGroup.items:
            skills.append((skill.ID, skill.name))
        return skills
