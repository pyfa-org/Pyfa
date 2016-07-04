type = "passive", "structure"
def handler(fit, src, context):
    groups = ("Structure Warp Scrambler", "Structure Disruption Battery", "Structure Stasis Webifier")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                    "capacitorNeed", src.getModifiedItemAttr("capNeedBonus"), skill="Structure Electronic Systems")
