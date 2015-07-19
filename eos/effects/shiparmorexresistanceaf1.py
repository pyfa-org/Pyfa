# shipArmorEXResistanceAF1
#
# Used by:
# Ship: Astero
# Ship: Malice
# Ship: Punisher
type = "passive"
def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("shipBonusAF"), skill="Amarr Frigate")
