# Used by:
# Subsystem: Tengu Electronics - Obfuscation Manifold
type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Caldari Electronic Systems").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "ECM",
                                  "maxRange", module.getModifiedItemAttr("subsystemBonusCaldariElectronic") * level)
