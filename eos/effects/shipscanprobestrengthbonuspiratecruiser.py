# Used by:
# Ship: Astero
# Ship: Gnosis
# Ship: Stratios
type = "passive"
def handler(fit, container, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", container.getModifiedItemAttr("shipBonusPirateFaction2"))
