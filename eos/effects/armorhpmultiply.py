# Used by:
# Modules from group: Armor Coating (202 of 202)
# Modules from group: Armor Plating Energized (187 of 187)
# Module: QA Multiship Module - 10 Players
# Module: QA Multiship Module - 20 Players
# Module: QA Multiship Module - 40 Players
# Module: QA Multiship Module - 5 Players
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("armorHP", module.getModifiedItemAttr("armorHPMultiplier"))