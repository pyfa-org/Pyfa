# Used by:
# Implant: Poteque 'Prospector' Environmental Analysis EY-1005
type = "passive"
def handler(fit, implant, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Salvager",
                                  "duration", implant.getModifiedItemAttr("durationBonus"))
