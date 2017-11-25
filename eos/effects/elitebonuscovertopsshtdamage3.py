# eliteBonusCovertOpsSHTDamage3
#
# Used by:
# Ship: Virtuoso
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Small Hybrid Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("eliteBonusCovertOps3"), skill="Covert Ops")
