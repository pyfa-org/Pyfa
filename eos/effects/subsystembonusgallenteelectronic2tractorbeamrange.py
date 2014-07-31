# Used by:
# Subsystem: Proteus Electronics - Emergent Locus Analyzer
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Gallente Electronic Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Tractor Beam",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusGallenteElectronic2") * level)
