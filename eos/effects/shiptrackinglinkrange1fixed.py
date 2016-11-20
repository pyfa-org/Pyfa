# shipTrackingLinkRange1Fixed
#
# Used by:
# Ship: Scimitar
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusMC"), skill="Minmatar Cruiser")
