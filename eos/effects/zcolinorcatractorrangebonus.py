type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam", "maxRange", src.getModifiedItemAttr("roleBonusTractorBeamRange"), stackingPenalties=True)
