# Used by:
# Implant: Grail Alpha
# Implant: Grail Beta
# Implant: Grail Delta
# Implant: Grail Epsilon
# Implant: Grail Gamma
# Implant: Jackal Alpha
# Implant: Jackal Beta
# Implant: Jackal Delta
# Implant: Jackal Epsilon
# Implant: Jackal Gamma
# Implant: Spur Alpha
# Implant: Spur Beta
# Implant: Spur Delta
# Implant: Spur Epsilon
# Implant: Spur Gamma
# Implant: Talon Alpha
# Implant: Talon Beta
# Implant: Talon Delta
# Implant: Talon Epsilon
# Implant: Talon Gamma
type = "passive"
def handler(fit, implant, context):
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        sensorType = "scan{0}Strength".format(type)
        sensorBoost = "scan{0}StrengthPercent".format(type)
        if sensorBoost in implant.item.attributes:
            fit.ship.boostItemAttr(sensorType, implant.getModifiedItemAttr(sensorBoost))
