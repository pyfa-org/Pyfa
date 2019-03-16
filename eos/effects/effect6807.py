# invulnerabilityCoreDurationBonus
#
# Used by:
# Skill: Invulnerability Core Operation
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Invulnerability Core Operation"), "buffDuration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Invulnerability Core Operation"), "duration",
                                  src.getModifiedItemAttr("durationBonus") * lvl)
