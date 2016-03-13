# shipRocketExpDmgMF3
#
# Used by:
# Ship: Vigil Fleet Issue
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"), "explosiveDamage", src.getModifiedItemAttr("shipBonus3MF"), skill="Minmatar Frigate")
