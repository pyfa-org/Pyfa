# subsystemBonusAmarrCore2EnergyVampireAmount
#
# Used by:
# Subsystem: Legion Core - Energy Parasitic Complex
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Nosferatu", "powerTransferAmount",
                                  src.getModifiedItemAttr("subsystemBonusAmarrCore2"), skill="Amarr Core Systems")
