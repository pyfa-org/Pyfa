# subsystemBonusCaldariCore3ECMHeatBonus
#
# Used by:
# Subsystem: Tengu Core - Obfuscation Manifold
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM", "overloadECMStrengthBonus",
                                  src.getModifiedItemAttr("subsystemBonusCaldariCore3"), skill="Caldari Core Systems")
