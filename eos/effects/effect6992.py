# roleBonusMHTDamage1
#
# Used by:
# Ship: Victor
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Medium Hybrid Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusRole1"))
