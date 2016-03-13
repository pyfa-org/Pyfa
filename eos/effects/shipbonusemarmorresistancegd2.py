# shipBonusEMArmorResistanceGD2
#
# Used by:
# Ship: Magus
type = "passive"
def handler(fit, src, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("shipBonusGD2"), skill="Gallente Destroyer")
