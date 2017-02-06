# Not used by any item
type = "passive"


def handler(fit, module, context):
    # Note: we increase maxGroupActive by two.
    # If we only increased it by one, we'd get the number to stay equal
    # As Comman Processors use one themselves too
    fit.modules.filteredItemIncrease(lambda mod: mod.item.group.name == "Gang Coordinator" and
                                                 "maxGroupActive" in mod.itemModifiedAttributes,
                                     "maxGroupActive", 1)
