# cynosuralDurationBonus
#
# Used by:
# Ships from group: Force Recon Ship (5 of 6)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cynosural Field",
                                  "duration", ship.getModifiedItemAttr("durationBonus"))
