# implantVelocityBonus
#
# Used by:
# Implants named like: Eifyr and Co. 'Rogue' Navigation NN (6 of 6)
# Implant: Genolution Core Augmentation CA-3
# Implant: Shaqil's Speed Enhancer
type = "passive"


def handler(fit, implant, context):
    fit.ship.boostItemAttr("maxVelocity", implant.getModifiedItemAttr("implantBonusVelocity"))
