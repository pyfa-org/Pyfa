# Not used by any item
type = "passive"
runTime = "early"


def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Remote Armor Repair Systems"),
                                  "armorDamageAmount", module.getModifiedItemAttr("subsystemBonusGallenteDefensive2"),
                                  skill="Gallente Defensive Systems")
