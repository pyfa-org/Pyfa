# subsystemBonusAmarrPropulsion2MWDPenalty
#
# Used by:
# Subsystem: Legion Propulsion - Wake Limiter
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", src.getModifiedItemAttr("subsystemBonusAmarrPropulsion2"),
                                  skill="Amarr Propulsion Systems")
