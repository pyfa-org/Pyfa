# Used by:
# Subsystem: Loki Electronics - Immobility Drivers
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Electronic Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Stasis Web",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusMinmatarElectronic") * level)
