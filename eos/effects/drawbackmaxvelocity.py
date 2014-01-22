# Used by:
# Modules named like: Anti Pump (32 of 32)
# Modules named like: Remote Augmentor (8 of 8)
# Modules named like: Salvage Tackle (8 of 8)
# Modules named like: Trimark Pump (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("drawback"),
                           stackingPenalties = True)