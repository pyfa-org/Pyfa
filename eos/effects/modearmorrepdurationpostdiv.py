type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(
        lambda mod: mod.item.requiresSkill("Repair Systems"),
        "duration",
        1 / module.getModifiedItemAttr("modeArmorRepDurationPostDiv")
    )
