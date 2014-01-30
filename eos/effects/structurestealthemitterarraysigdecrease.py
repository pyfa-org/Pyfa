# Used by:
# Implant: Halo Alpha
# Implant: Halo Beta
# Implant: Halo Delta
# Implant: Halo Epsilon
# Implant: Halo Gamma
# Implant: Improved X-Instinct Booster
# Implant: Low-grade Halo Alpha
# Implant: Low-grade Halo Beta
# Implant: Low-grade Halo Delta
# Implant: Low-grade Halo Epsilon
# Implant: Low-grade Halo Gamma
# Implant: Standard X-Instinct Booster
# Implant: Strong X-Instinct Booster
# Implant: Synth X-Instinct Booster
type = "passive"
def handler(fit, implant, context):
    fit.ship.boostItemAttr("signatureRadius", implant.getModifiedItemAttr("signatureRadiusBonus"))
