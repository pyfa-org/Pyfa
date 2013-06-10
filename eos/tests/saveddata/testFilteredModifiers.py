from eos.tests import TestBase
from eos import db
from eos.types import Fit

class Test(TestBase):
    def setUp(self):
        TestBase.setUp(self)
        self.f = Fit()
        self.i1 = db.getItem("Cyclops")
        self.i2 = db.getItem("Cyclops")
        self.charge = db.getItem("Compact Purgatory Torpedo I")
        self.f.drones.appendItem(self.i1, 1)
        self.f.drones.appendItem(self.i2, 1)

    def test_filteredItemIncrease(self):
        self.f.drones.filteredItemIncrease(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i1.getAttribute("hp") + 5)
            else:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i2.getAttribute("hp"))


    def test_filteredItemMultiply(self):
        self.f.drones.filteredItemMultiply(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i1.getAttribute("hp") * 5)
            else:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i2.getAttribute("hp"))


    def test_filteredItemBoost(self):
        self.f.drones.filteredItemBoost(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i1.getAttribute("hp") * 1.05)
            else:
                self.assertEquals(d.itemModifiedAttributes["hp"], self.i2.getAttribute("hp"))

    def test_filteredChargeIncrease(self):
        self.f.drones.filteredChargeIncrease(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp") + 5)
            else:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp"))


    def test_filteredChargeMultiply(self):
        self.f.drones.filteredChargeMultiply(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp") * 5)
            else:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp"))


    def test_filteredChargeBoost(self):
        self.f.drones.filteredChargeBoost(lambda d: d.item.ID == self.i1.ID, "hp", 5)
        for d in self.f.drones:
            if d.item.ID == self.i1.ID:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp") * 1.05)
            else:
                self.assertEquals(d.chargeModifiedAttributes["hp"], self.charge.getAttribute("hp"))
