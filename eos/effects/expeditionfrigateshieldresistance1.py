# expeditionFrigateShieldResistance1
#
# Used by:
# Ship: Endurance
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                           skill="Expedition Frigates")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                           skill="Expedition Frigates")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                           skill="Expedition Frigates")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("eliteBonusExpedition1"),
                           skill="Expedition Frigates")
