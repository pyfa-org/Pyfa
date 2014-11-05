# shipArmorEMResistanceRookie
#
# Used by:
# Ship: Devoter
# Ship: Impairor
# Ship: Phobos
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))
