# Used by:
# Ship: Scimitar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Cruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Shield Transporter",
                                  "shieldTransferRange", ship.getModifiedItemAttr("shipBonusMC2") * level)
