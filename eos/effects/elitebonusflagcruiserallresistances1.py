# eliteBonusFlagCruiserAllResistances1
#
# Used by:
# Ship: Monitor
type = "passive"


def handler(fit, src, context):
    fit.ship.boostItemAttr("explosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("shieldKineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("shieldExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("armorThermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("thermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("shieldEmDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("armorExplosiveDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("armorEmDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("shieldThermalDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("kineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("armorKineticDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
    fit.ship.boostItemAttr("emDamageResonance", src.getModifiedItemAttr("eliteBonusFlagCruisers1"), skill="Flag Cruisers")
