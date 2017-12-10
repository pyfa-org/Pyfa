# eliteBonusCoverOpsNOSNeutFalloff1
#
# Used by:
# Ship: Caedes
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Energy Nosferatu", "Energy Neutralizer"),
                                  "falloffEffectiveness", src.getModifiedItemAttr("eliteBonusCovertOps1"),
                                  stackingPenalties=True, skill="Covert Ops")
