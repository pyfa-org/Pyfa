"""
Since fighter abilities do not have any sort of item entity in the EVE database, we must derive the abilities from the
effects, and thus this effect file contains some custom information useful only to fighters.
"""
# User-friendly name for the ability
displayName = "Bomb"

# Attribute prefix that this ability targets
prefix = "fighterAbilityLaunchBomb"

type = "active"

def handler(fit, src, context):
    pass