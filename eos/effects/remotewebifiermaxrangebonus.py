# remoteWebifierMaxRangeBonus
#
# Used by:
# Implants named like: Inquest 'Eros' Stasis Webifier MR (3 of 3)
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web", "maxRange",
                                  src.getModifiedItemAttr("stasisWebRangeBonus"), stackingPenalties=True)
