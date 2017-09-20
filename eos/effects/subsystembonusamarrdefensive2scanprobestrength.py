type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"),
                                    "baseSensorStrength", src.getModifiedItemAttr("subsystemBonusAmarrDefensive2"),
                                    skill="Amarr Defensive Systems")
