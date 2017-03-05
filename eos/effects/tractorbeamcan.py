# tractorBeamCan
#
# Used by:
# Modules from group: Tractor Beam (4 of 4)
type = "active"
from eos.config import settings

def handler(fit, module, context):
    print settings['setting1']
    pass
