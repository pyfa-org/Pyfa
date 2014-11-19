# shipArmorRepairingRookie
#
# Used by:
# Ship: Velator
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", ship.getModifiedItemAttr("rookieArmorRepBonus"))
