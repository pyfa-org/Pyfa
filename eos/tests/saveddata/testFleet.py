from eos.tests import TestBase
from eos import db
from eos.types import Fleet, Wing, Squad, Ship, Fit, Module, Character
import copy

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        g = Fleet()
        w = Wing()
        s = Squad()
        self.g = g
        self.s = s
        self.w = w
        g.wings.append(w)
        w.squads.append(s)
        f = Fit()
        self.s.members.append(f)
        self.s.members.append(Fit())
        self.s.leader = f
        f.ship = Ship(db.getItem("Rifter"))
        f.character = Character("testety")
        f.character.getSkill("Leadership").level = 5

    def test_copy(self):
        c = copy.deepcopy(self.g)
        self.assertNotEquals(id(c), id(self.g))
        self.assertEquals(len(c.wings), 1)
        wing = c.wings[0]
        self.assertNotEquals(id(wing), id(self.w))
        self.assertEquals(len(wing.squads), 1)
        squad = wing.squads[0]
        self.assertNotEquals(id(squad), id(self.s))
        self.assertEquals(len(squad.members), 2)

    def test_skillGang(self):
        self.s.leader.character.getSkill("Leadership").level = 5
        self.g.calculateModifiedAttributes()
        new = self.s.leader.ship.getModifiedItemAttr("scanResolution")
        expected = self.s.leader.ship.item.getAttribute("scanResolution") * 1.1
        self.assertEquals(expected, new)

    def test_gangModGang(self):
        self.s.leader.modules.append(Module(db.getItem("Siege Warfare Link - Shield Harmonizing")))
        self.g.calculateModifiedAttributes()
        expected = self.s.leader.ship.item.getAttribute("shieldKineticDamageResonance") * 0.98
        new = self.s.leader.ship.getModifiedItemAttr("shieldKineticDamageResonance")
        self.assertEquals(expected, new)

    def test_shipGang(self):
        self.s.leader.character.getSkill("Gallente Titan").level = 1
        self.s.leader.ship = Ship(db.getItem("Erebus"))
        self.g.calculateModifiedAttributes()
        new = self.s.leader.ship.getModifiedItemAttr("armorHP")
        expected = self.s.leader.ship.item.getAttribute("armorHP") * 1.075
        self.assertEquals(expected, new)

    def test_onlyFC(self):
        self.g.leader = Fit()
        self.g.leader.ship = Ship(db.getItem("Rifter"))
        self.g.leader.character = Character("tootoot")
        self.g.leader.character.getSkill("Leadership").level = 5
        self.g.calculateModifiedAttributes()
        self.assertEquals(self.g.leader.ship.item.getAttribute("scanResolution"), self.g.leader.ship.getModifiedItemAttr("scanResolution"))
        self.assertEquals(self.s.leader.ship.item.getAttribute("scanResolution") * 1.1, self.s.leader.ship.getModifiedItemAttr("scanResolution"))

    def test_onlyWC(self):
        self.w.leader = Fit()
        self.w.leader.ship = Ship(db.getItem("Rifter"))
        self.w.leader.character = Character("tootoot")
        self.w.leader.character.getSkill("Leadership").level = 5
        self.w.leader.character.getSkill("Wing Command").level = 5
        self.g.calculateModifiedAttributes()
        self.assertEquals(self.s.leader.ship.item.getAttribute("scanResolution") * 1.1, self.s.leader.ship.getModifiedItemAttr("scanResolution"))
        self.assertEquals(self.w.leader.ship.item.getAttribute("scanResolution") * 1.1, self.w.leader.ship.getModifiedItemAttr("scanResolution"))
