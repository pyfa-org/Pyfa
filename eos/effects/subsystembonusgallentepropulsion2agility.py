type = "passive"
def handler(fit, src, context):
    # @ todo: CCP fucked up, the proteus chassis optimization subsystem has the minmatar attribute, not gallente
    return
    fit.ship.boostItemAttr("agility", src.getModifiedItemAttr("subsystemBonusGallentePropulsion2"),
                           skill="Gallente Propulsion Systems")
