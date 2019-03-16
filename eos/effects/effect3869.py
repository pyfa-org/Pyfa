# subsystemBonusMinmatarPropulsion2MWDPenalty
#
# Used by:
# Subsystem: Loki Propulsion - Wake Limiter
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", src.getModifiedItemAttr("subsystemBonusMinmatarPropulsion2"),
                                  skill="Minmatar Propulsion Systems")
