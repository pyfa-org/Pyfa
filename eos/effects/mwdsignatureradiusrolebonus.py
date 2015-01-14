# MWDSignatureRadiusRoleBonus
#
# Used by:
# Ships from group: Assault Frigate (8 of 12)
# Ships from group: Heavy Assault Cruiser (10 of 13)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("MWDSignatureRadiusBonus"))
