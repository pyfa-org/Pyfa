type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Astrometrics"), "baseSensorStrength", src.getModifiedItemAttr("subsystemBonusCaldariDefensive2"), stackingPenalties=True, skill="Caldari Defensive Systems")
