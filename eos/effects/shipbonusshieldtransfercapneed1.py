# Used by:
# Ship: Osprey
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Transporter",
                                  "capacitorNeed", ship.getModifiedItemAttr("shipBonusCC") * level)
