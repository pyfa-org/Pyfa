import wx
import gui.mainFrame

def formatTable(valList, numColumns):

    damageProfileList.append(["[NPC][Other] Sleepers", "1472", "1472", "1384", "1384"])
    damageProfileList.append(["[NPC][Other] Sansha Incursion", "1682", "1347", "3678", "3678"])

    for valueRow in valList:
        name, em, therm, kin, exp = valueRow
        damageProfile = eos.db.getDamagePattern(name)
        if damageProfile is None:
            damageProfile = eos.types.DamagePattern(em, therm, kin, exp)
            damageProfile.name = name
            eos.db.save(damageProfile)

    for miningType, image in (("miner", "mining"), ("drone", "drones")):
        baseBox = wx.BoxSizer(wx.HORIZONTAL)
        sizerMiningYield.Add(baseBox, 1, wx.ALIGN_LEFT if counter == 0 else wx.ALIGN_CENTER_HORIZONTAL)

        # baseBox.Add(BitmapLoader.getStaticBitmap("%s_big" % image, parent, "gui"), 0, wx.ALIGN_CENTER)

        box = wx.BoxSizer(wx.VERTICAL)
        baseBox.Add(box, 0, wx.ALIGN_CENTER)
        baseBox.Add()

        lbl = wx.StaticText(parent, wx.ID_ANY, u"0.0 m\u00B3/s")
        setattr(self, "label%sminingyield%s" % (panel.capitalize(), miningType.capitalize()), lbl)

        box.Add(wx.StaticText(parent, wx.ID_ANY, miningType.capitalize() + ": "), 0, wx.ALIGN_LEFT)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(hbox, 1, wx.ALIGN_CENTER)

        box.Add(lbl, 0, wx.ALIGN_CENTER)
        self._cachedValues.append(0)
        counter += 1