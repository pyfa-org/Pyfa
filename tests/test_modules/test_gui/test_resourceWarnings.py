import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from gui.utils.resourceWarnings import is_calibration_over_limit


def test_calibration_equal_limit_is_not_warning():
    assert is_calibration_over_limit(400, 400) is False


def test_calibration_over_limit_is_warning():
    assert is_calibration_over_limit(401, 400) is True


def test_calibration_float_precision_not_warning_at_equal_display_value():
    # Values below total should not trigger warning.
    assert is_calibration_over_limit(399.9999999, 400) is False


def test_calibration_float_precision_warning_when_meaningfully_above_limit():
    assert is_calibration_over_limit(400.01, 400) is True


def test_calibration_none_values_are_safe():
    assert is_calibration_over_limit(None, 400) is False
    assert is_calibration_over_limit(450, None) is True
