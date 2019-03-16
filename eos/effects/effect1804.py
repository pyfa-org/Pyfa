# shipArmorEMResistanceAF1
#
# Used by:
# Ship: Astero
# Ship: Malice
# Ship: Punisher
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorEmDamageResonance", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
