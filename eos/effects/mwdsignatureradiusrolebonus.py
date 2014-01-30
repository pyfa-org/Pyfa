# Used by:
# Items from market group: Ships > Cruisers > Advanced Cruisers > Heavy Assault Cruisers (8 of 8)
# Items from market group: Ships > Frigates > Advanced Frigates > Assault Frigates (8 of 8)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("High Speed Maneuvering"),
                                  "signatureRadiusBonus", ship.getModifiedItemAttr("MWDSignatureRadiusBonus"))
