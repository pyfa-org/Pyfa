# shipBonusForceAuxiliaryM3CapBoosterStrength
#
# Used by:
# Ship: Lif
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.group.name == "Capacitor Booster Charge", "capacitorBonus", src.getModifiedItemAttr("shipBonusForceAuxiliaryM3"), skill="Minmatar Carrier")
