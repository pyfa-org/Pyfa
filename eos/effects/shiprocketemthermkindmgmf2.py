# shipRocketEMThermKinDmgMF2
#
# Used by:
# Ship: Vigil Fleet Issue
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "emDamage",
                                    src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "thermalDamage",
                                    src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "kineticDamage",
                                    src.getModifiedItemAttr("shipBonusMF2"), skill="Minmatar Frigate")
