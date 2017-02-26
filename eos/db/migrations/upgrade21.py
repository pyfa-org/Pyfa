"""
Migration 21

- Fixes discrepancy in drone table where we may have an amount active that is not equal to the amount in the stack
  (we don't support activating only 2/5 drones). See GH issue #728
"""


def upgrade(saveddata_engine):
    saveddata_engine.execute("UPDATE drones SET amountActive = amount where amountActive > 0 AND amountActive <> amount;")
