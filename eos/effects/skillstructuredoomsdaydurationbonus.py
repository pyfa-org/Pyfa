type = "passive", "structure"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Structure Doomsday Weapon",
                                    "duration", src.getModifiedItemAttr("durationBonus"), skill="Structure Doomsday Operation")
