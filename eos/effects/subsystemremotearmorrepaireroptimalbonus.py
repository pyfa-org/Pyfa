type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in ("Remote Armor Repairer",  "Ancillary Remote Armor Repairer"),
                                  "maxRange", src.getModifiedItemAttr("remoteArmorRepairerOptimalBonus"))

