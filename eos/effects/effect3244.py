# eliteBonusGunshipArmorExplosiveResistance1
#
# Used by:
# Ship: Vengeance
type = "passive"


def handler(fit, ship, context):
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", ship.getModifiedItemAttr("eliteBonusGunship1"),
                           skill="Assault Frigates")
