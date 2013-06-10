# Used by:
# Ship: Freki
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusATF1"))
