# eliteBonusLogisticsTrackingLinkTrackingSpeedBonus2
#
# Used by:
# Ship: Oneiros
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("eliteBonusLogistics2"),
                                  skill="Logistics Cruisers")
