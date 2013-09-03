# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Logistics").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Tracking Computer",
                                  "trackingSpeedBonus", ship.getModifiedItemAttr("eliteBonusLogistics1") * level)
