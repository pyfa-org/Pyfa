def is_calibration_over_limit(used_points, total_points):
    """
    Decide when calibration values should be shown as warning (red).
    Warn only when used points are meaningfully above total points.
    """
    used = 0.0 if used_points is None else float(used_points)
    total = 0.0 if total_points is None else float(total_points)
    return (used - total) > 1e-6
