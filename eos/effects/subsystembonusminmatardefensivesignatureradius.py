# subsystemBonusMinmatarDefensiveSignatureRadius
#
# Used by:
# Subsystem: Loki Defensive - Amplification Node
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("subsystemBonusMinmatarDefensive"), skill="Minmatar Defensive Systems")
