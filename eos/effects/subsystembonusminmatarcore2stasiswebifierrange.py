# subsystemBonusMinmatarCore2StasisWebifierRange
#
# Used by:
# Subsystem: Loki Core - Immobility Drivers
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", src.getModifiedItemAttr("subsystemBonusMinmatarCore2"), skill="Minmatar Core Systems")
