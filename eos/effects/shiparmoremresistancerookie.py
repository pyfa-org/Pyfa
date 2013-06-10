# Used by:
# Ship: Impairor
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("rookieArmorResistanceBonus"))
