# Used by:
# Modules from group: Gyrostabilizer (20 of 20)
# Module: QA Damage Module
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Projectile Weapon",
                                  "damageMultiplier", module.getModifiedItemAttr("damageMultiplier"),
                                  stackingPenalties = True)