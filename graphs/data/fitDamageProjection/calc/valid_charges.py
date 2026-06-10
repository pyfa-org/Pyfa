# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import eos.db
from eos.gamedata import Item


# Class-level cache for valid charges: {itemID: set(charges)}
# This prevents repeated DB queries for the same module type
_validChargesCache = {}


def getValidChargesForModule(module):
    """
    Get all valid charges for a module using optimized database query.
    
    This is a performance-optimized version for graph calculations that:
    1. Uses class-level caching to prevent repeated queries for the same module type
    2. Uses direct SQLAlchemy queries instead of eager loading full groups
    3. Only validates published items that match the charge groups
    
    Args:
        module: The Module instance to get valid charges for
        
    Returns:
        set: Set of valid Item instances that can be used as charges
    """
    # Check class-level cache first
    if module.item.ID in _validChargesCache:
        return _validChargesCache[module.item.ID].copy()
    
    # Collect all charge group IDs for this module
    chargeGroupIDs = []
    for i in range(5):
        itemChargeGroup = module.getModifiedItemAttr('chargeGroup' + str(i), None)
        if itemChargeGroup:
            chargeGroupIDs.append(int(itemChargeGroup))
    
    if not chargeGroupIDs:
        _validChargesCache[module.item.ID] = set()
        return set()
    
    # Query only published items from the relevant charge groups
    # This is much more efficient than loading entire groups with all attributes
    session = eos.db.get_gamedata_session()
    
    # Query published items in the relevant groups
    # Note: We let attributes lazy-load only when needed by isValidCharge()
    items = session.query(Item).filter(
        Item.groupID.in_(chargeGroupIDs),
        Item.published == True
    ).all()
    
    # Validate each item with the module's size/capacity constraints
    validCharges = set()
    for item in items:
        if module.isValidCharge(item):
            validCharges.add(item)
    
    # Store in class-level cache
    _validChargesCache[module.item.ID] = validCharges
    return validCharges.copy()

