import os
import sys
import mock
from unittest.mock import MagicMock

# Add root folder to python paths
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..', '..')))

from eos.effects import Effect7166
from eos.const import FittingModuleState

def test_pulse_inactive_afflictors(RifterFit):
    """
    Test that getPulseInactiveAfflictorsAt correctly identifies inactive modules
    during the wait period of a pulse cycle.
    """
    fit = RifterFit
    
    # Get a module (e.g. 200mm Steel Plates, though that's passive. Let's find an active one or add one)
    # RifterFit usually comes with some modules. Let's assume we can add one.
    
    # We will mock a module for simplicity of testing strictly the time logic
    # or we can use a real module if we knew the ID.
    # Let's inspect RifterFit modules in the test? No, let's just make a mock module inside the fit.
    
    # Create a mock module structure
    mod = MagicMock()
    mod.state = FittingModuleState.ACTIVE
    mod.pulseInterval = 10.0 # Pulse every 10 seconds
    mod.getModifiedItemAttr = MagicMock(return_value=5000.0) # 5s duration
    
    # Set properties used by getPulseInactiveAfflictorsAt
    mod.rawCycleTime = 5000
    mod.pulseAdjustedCycleTime = 10000
    
    # The method calls self.getModifiedItemAttr('duration')
    # wait, getPulseInactiveAfflictorsAt calls:
    # duration = mod.getModifiedItemAttr('duration')
    # which returns milliseconds? usually traits are in ms.
    
    # Let's verify unit of duration in fit.py
    # "cycleTime = mod.getModifiedItemAttr('duration')"
    
    mod.getModifiedItemAttr.side_effect = lambda x: 5000.0 if x == 'duration' else 0
    mod.fit = fit
    
    # Replace fit modules with our mock list for this test
    # We patch the property 'modules' on the Fit class to return our list.
    with mock.patch('eos.saveddata.fit.Fit.modules', new_callable=mock.PropertyMock) as mock_modules:
        mock_modules.return_value = [mod]
        
        # Case 1: Time = 1s (Inside Cycle)
        # 1000 % 10000 = 1000. 1000 < 5000. Active.
        inactive = fit.getPulseInactiveAfflictorsAt(1000)
        assert mod not in inactive
        
        # Case 2: Time = 6s (Wait Phase)
        # 6000 % 10000 = 6000. 6000 > 5000. Inactive.
        inactive = fit.getPulseInactiveAfflictorsAt(6000)
        assert mod in inactive
        
        # Case 3: Time = 11s (Next Cycle)
        # 11000 % 10000 = 1000. 1000 < 5000. Active.
        inactive = fit.getPulseInactiveAfflictorsAt(11000)
        assert mod not in inactive


def test_projected_spool_reset_logic():
    """
    Test that Effect7166 (Mutadaptive Remote Armor Repairer) forces SpoolAmount to 0
    when the source module has a pulse interval set (and gap exists).
    """
    
    # Mock Fit and Ship
    mock_fit = MagicMock()
    mock_fit.ship.getModifiedItemAttr.return_value = False # disallowAssistance = False
    mock_fit._armorRr = []
    mock_fit._armorRrPreSpool = []
    mock_fit._armorRrFullSpool = []
    
    # Mock Container (The Module)
    mock_container = MagicMock()
    mock_container.getModifiedItemAttr.side_effect = lambda x: {
        'armorDamageAmount': 100,
        'maxRange': 10000,
        'falloffEffectiveness': 1000,
        'duration': 5000, # 5s
        'repairMultiplierBonusMax': 1.0, # 100% bonus
        'repairMultiplierBonusPerCycle': 0.1 # 10% per cycle
    }.get(x, 0)
    
    # Mock Context
    context = {'projected': True}
    
    # Mock Config
    # Also mock resolveSpoolOptions to return a known high spool amount (1.0 = 100% bonus)
    # This isolates the test from user config/defaults/options logic.
    from eos.utils.spoolSupport import SpoolType
    with mock.patch('eos.config.settings', {'globalDefaultSpoolupPercentage': 1.0}), \
         mock.patch('eos.effects.resolveSpoolOptions', return_value=(SpoolType.SPOOL_SCALE, 1.0)):
        
        # Scenario 1: No Pulsing
        # Spool should default to Max (1.0) because we mocked resolveSpoolOptions
        mock_container.pulseInterval = None
        Effect7166.handler(mock_fit, mock_container, context, 5000)
        
        # Resolution should be full spool
        # Base 100 * (1 + 1.0) = 200
        result_amount = mock_fit._armorRr[-1][0]
        # Check tolerance (float math)
        assert abs(result_amount - 200.0) < 0.1
        
        # Scenario 2: Pulsing Active (With Gap)
        # Pulse 10s (Duration 5s). Gap = 5s. Spool should reset to 0.
        mock_container.pulseInterval = 10.0
        Effect7166.handler(mock_fit, mock_container, context, 5000)
        
        # Resolution should be 0 spool
        # Base 100 * (1 + 0) = 100
        result_amount = mock_fit._armorRr[-1][0]
        assert abs(result_amount - 100.0) < 0.1

        # Scenario 3: Pulsing Active (No Gap / Constant)
        # Pulse 5s (Duration 5s). Gap = 0s. Spool should NOT reset.
        mock_container.pulseInterval = 5.0
        Effect7166.handler(mock_fit, mock_container, context, 5000)
        
        # Resolution should be full spool
        result_amount = mock_fit._armorRr[-1][0]
        assert abs(result_amount - 200.0) < 0.1
