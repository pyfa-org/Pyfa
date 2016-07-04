# targetAttack
#
# Used by:
# Citadel Point Defense
type = 'active'
def handler(fit, module, context):
    # Set reload time to 1 second
    module.reloadTime = 1000

# TODO
# believe this doesn't actual require skills to use.
# Need to figure out how to remove the skill req *OR* tie it to the structure.
# also doesn't have reload so...