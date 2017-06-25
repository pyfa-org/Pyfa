# subSystemBonusAmarrDefensiveTractorBeamBonus3
#
# Used by:
# Subsystem: Legion Defensive - Covert Reconfiguration
type = "passive"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                  skill="Amarr Defensive Systems")

    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxTractorVelocity", module.getModifiedItemAttr("subsystemBonusAmarrDefensive3"),
                                  skill="Amarr Defensive Systems")
