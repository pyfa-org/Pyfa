# shipArmorEMResistanceRookie
#
# Used by:
# Ship: Devoter
# Ship: Gold Magnate
# Ship: Impairor
# Ship: Phobos
# Ship: Silver Magnate
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))
