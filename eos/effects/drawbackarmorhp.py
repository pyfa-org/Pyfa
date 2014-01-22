# Used by:
# Modules named like: Auxiliary Thrusters (8 of 8)
# Modules named like: Cargohold Optimization (8 of 8)
# Modules named like: Engine I (8 of 8)
# Modules named like: Engine II (8 of 8)
# Modules named like: Low Nozzle (8 of 8)
# Modules named like: Valve (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("armorHP", module.getModifiedItemAttr("drawback"))