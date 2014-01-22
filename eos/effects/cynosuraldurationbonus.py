# Used by:
# Ship: Arazu
# Ship: Falcon
# Ship: Pilgrim
# Ship: Rapier
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Cynosural Field",
                                  "duration", ship.getModifiedItemAttr("durationBonus"))
